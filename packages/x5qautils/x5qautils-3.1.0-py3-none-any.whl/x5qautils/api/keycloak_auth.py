import asyncio
import re
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Coroutine, Dict, Union

import allure
from aiohttp import ClientResponse, ClientSession
from requests import Response

from . import content_type
from .log_request import log
from .microservices import RequestSession


@dataclass
class KeycloakAuth:
    """
    Работает для асинхронного и синхронного кода
    Для нормального и полноценного использования, надо отнаследоваться от класса
    и задать метод получения токена в своем приложении, он у всех будет отличаться
    например:
        def _add_token_api(self):
            result = self._get(https://portal.stage.bdsp.x5.ru/api/v1/public/auth/token')
            self.headers['X5-Api-Key'] = result['result']['token']
            return self
    """
    login: str
    passwd: str
    session: Union[RequestSession, ClientSession] = field(default_factory=RequestSession)
    loop: asyncio.AbstractEventLoop = None
    client_id: str = ''
    client_secret: str = ''
    url: str = ''
    _login_params: dict = None

    def __post_init__(self):
        self._login_params = {
            'client_id': self.client_id,
        }
        self.headers.update({'Content-Type': content_type.JSON})
        self.loop = self.loop or asyncio.get_event_loop()

    @property
    def headers(self):
        return self.session.headers

    @property
    def cookies(self):
        if isinstance(self.session, ClientSession):
            return self.session.cookie_jar
        return self.session.cookies

    def update_cookies(self, obj):
        if isinstance(self.session, ClientSession):
            self.cookies.update_cookies({cookie.key: cookie.value for cookie in obj.values()})
        else:
            self.cookies.update({cookie.name: cookie.value for cookie in obj})

    @cached_property
    def verify_kwargs(self):
        if isinstance(self.session, ClientSession):
            return {'ssl': False}
        return {'verify': False}

    def __enter__(self):
        return self

    def _run(self, obj: Union[Coroutine, Any]) -> Any:
        if isinstance(obj, Coroutine):
            return self.loop.run_until_complete(obj)
        return obj

    def _request(self, method, url, params=None, data=None, headers=None, not_json=False) \
            -> Union[Dict, Response, ClientResponse]:
        response = self._run(
            self.session.request(
                method, url, data=data, headers=headers, params=params, **self.verify_kwargs
            ))
        if not_json:
            return response
        return self._run(response.json())

    def _post(self, url, data=None, headers=None, params=None, not_json=False):
        return self._request('POST', url, params, data, headers, not_json)

    def _get(self, url, not_json=False):
        return self._request('GET', url, not_json=not_json)

    def _login(self, url):
        rr_1 = self._get(url, not_json=True)
        text = rr_1.text
        if isinstance(self.session, ClientSession):
            text = self._run(rr_1.text())  # noqa
        try:
            self._login_params = re.search(
                r'session_code=(?P<session_code>.*)&amp;execution=(?P<execution>.*)&amp;'
                r'client_id=(?P<client_id>.*?)&amp;tab_id=(?P<tab_id>.*?)"',
                text).groupdict()
        except AttributeError:
            allure.attach(text, attachment_type=allure.attachment_type.HTML)
            raise
        return self

    def _auth(self):
        pass

    def _add_cookies(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        realm = 'dialog-test'
        data = {
            'username': self.login,
            'password': self.passwd,
            'credentialId': ''
        }
        result = self._post(
            f'https://keycloak.do.x5.ru/auth/realms/{realm}/login-actions/authenticate',
            headers=headers,
            data=data,
            params=self._login_params,
            not_json=True
        )
        log.debug(result)
        for response in result.history:
            self.update_cookies(response.cookies)

        return self

    def _add_token_api(self):
        return self

    def auth(self, url=None):
        url = url or self.url

        self._login(url) \
            ._add_cookies() \
            .headers.update(
            {
                'Content-Type': content_type.JSON,
                'Accept': content_type.JSON,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
                'User-Agent': 'python-requests/2.25.1',
                'Connection': 'keep-alive',
            })
        self._add_token_api()

        log.info('Auth in keycloak with login %s', self.login)
        return self.session

    def _get_secret_cookie(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {"grant_type": "password",
                "username": self.login,
                "password": self.passwd,
                "client_id": self.client_id,
                "client_secret": self.client_secret}
        response = self._post('https://keycloak.do.x5.ru/auth/realms/LDAP_test/protocol/openid-connect/token',
                              data=data, headers=headers)
        return {"kc-access": response['access_token'], 'kc-state': response['refresh_token']}

    def auth_with_secret(self):
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        secret_cookie = self._get_secret_cookie()
        self.session.cookies['kc-access'] = secret_cookie['kc-access']
        self.session.cookies['kc-state'] = secret_cookie['kc-state']
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        del self.session
