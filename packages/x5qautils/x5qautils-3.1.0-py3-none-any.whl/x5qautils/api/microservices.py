import os
import textwrap
from dataclasses import dataclass, field
from functools import wraps
from http import HTTPStatus
from io import BufferedReader
from json import JSONDecodeError, dumps
from mimetypes import guess_extension
from pathlib import Path
from secrets import token_urlsafe
from typing import Dict, Type, Union

import allure
from aiohttp import ClientResponse
from furl import furl
from pydantic import ValidationError
from requests import Response, Session, TooManyRedirects

from .log_request import log, log_request
from .model import BaseAPI, BasePydantic, CodeError
from ..exceptions import AuthError, JSONValidationError, StatusCodeError
from ..helpers import attach_json, to_json_valid


def prepare(f):  # noqa C901
    @wraps(f)
    def wrapper(self, method, url, cls, params=None, data=None, json=None, headers=None, full_url='', **kwargs):
        if isinstance(url, str) and not furl(url).scheme:
            url = (self.furl / url).url
        elif isinstance(url, furl):
            url = url.url
        url = url or full_url

        if data and json:
            raise ValueError('Not used data and json')

        if data:
            if isinstance(data, BasePydantic):
                data = data.json()
            elif isinstance(data, (list, dict)):
                data = dumps(data)

        if json:
            json = to_json_valid(json)

        return f(self, method, url, cls, params=params, headers=headers, json=json, data=data, **kwargs)

    return wrapper


class RequestSession(Session):
    def resolve_redirects(self, resp: Response, *args, **kwargs):
        try:
            return super().resolve_redirects(resp, *args, **kwargs)
        except TooManyRedirects:
            attach_json([(r.status_code, r.url, r.text) for r in resp.history], name='Redirects log')
            raise


@dataclass
class MicroservicesTemplate:
    """

    """
    base_url: str
    session: Session = field(default_factory=RequestSession)
    cookies: dict = field(default_factory=dict)
    suffix: str = ''
    json_data: str = 'result'
    error_model: Type[BasePydantic] = CodeError

    def __post_init__(self):
        self.session.cookies.update(self.cookies)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @property
    def furl(self):
        return furl(f'{self.base_url}') / self.suffix

    @property
    def headers(self):
        return self.session.headers

    # Tools #####################################
    def _result(self, response):
        if response.status_code == HTTPStatus.NO_CONTENT:
            return  # noqa R502
        result = response.json()
        if isinstance(result, dict):
            assert result.get('code', 'ok') == 'ok'
            return result.get(self.json_data, result)
        return result

    @staticmethod
    def _get_text(response):
        return textwrap.shorten(textwrap.fill(response.text, response.status_code), response.status_code + 10)

    def _validation(
            self,
            response: Union[Response, ClientResponse],
            byte=False,
            text=None,
            valid_status_codes=tuple()
    ) -> Union[Dict, bytes]:
        text = text or response.text
        log_text = textwrap.shorten(textwrap.fill(text, response.status_code), response.status_code + 10)

        log.info('Result status code: %s time: %s %s',
                 response.status_code,
                 response.elapsed,
                 log_text
                 )
        log.debug('Full response:\n%s', text)
        valid_status_codes = (
            *valid_status_codes,
            HTTPStatus.CREATED,
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT
        )
        if response.status_code not in valid_status_codes:
            try:
                err = self.error_model.parse_raw(text)
            except (ValidationError, JSONValidationError):
                err = text
            raise StatusCodeError(
                f'Status code for {response.request.method}: {response.url},'
                f' status code: response {response.status_code}',
                err
            )

        if 'keycloak' in str(response.url) or response.status_code == 401:
            raise AuthError('Не прошла авторизация')
        if byte:
            return response.content

        return self._result(response)

    @prepare
    @log_request
    def _request(  # noqa C901
            self,
            method,
            url,
            model_response: Union[BaseAPI, BasePydantic, None] = None,
            params=None,
            data=None,
            json=None,
            headers=None,
            byte=False,
            path=None,
            valid_status_codes=tuple(),
            **kwargs
    ):
        with allure.step(f'{method.upper()} {url}'):
            response = self.session.request(
                method,
                url,
                params,
                data,
                json=json,
                headers=headers,
                verify=False,
                **kwargs
            )
            if isinstance(data, BufferedReader):
                attach_json(data.name, name='Request payload')
            elif data or json:
                attach_json(data or json, name='Request payload')

            with allure.step('Check response'):
                result = self._validation(response, byte=byte or path, valid_status_codes=valid_status_codes)

            if path:
                if isinstance(path, str):
                    path = Path(path)
                elif isinstance(path, bool):
                    path = Path(
                        os.getenv('PWD'),
                        f'tmp_{token_urlsafe(10)}{guess_extension(response.headers["Content-Type"])}'
                    )

                with allure.step(f'Сохраняем файл в {path}'):
                    with open(path, 'wb') as f:
                        f.write(response.content)

                return path

            if byte or model_response is None:
                attach_json(result, name='Result')
                return result

            try:
                attach_json(result, name='Result')
                attach_json(model_response.schema_json(by_alias=True, indent=4), name='Схема для Валидации ответа')
                return model_response.init(result)
            except ValidationError as e:
                err = e.json(indent=4)
                attach_json(err, name='Validation error')
                raise JSONValidationError(err)
            except JSONDecodeError:
                if guess_extension(response.headers['Content-Type']):
                    raise JSONValidationError(
                        '''Бинарный файл не может быть просто раскодирован в json
                           Используйте флаг byte=True, для получения бинарного результата
                           Или укажите path=Path(..)|"path/to_file.extension"|True - для сохранения результата
                        ''')
                raise JSONValidationError('Ответ не является валидным json')

    def get(self, url, model_response=None, /, params=None, **kwargs):
        """
        :param url: str or furl or path url
        :param model_response: (optional) sub class Optional[BaseAPI, BasePydantic]
        :param params: (optional) List or Dictionary or bytes to be sent in the query
        :param byte: return byte response
        :param path: save file path
        :param kwargs: Optional arguments that ``_request`` takes.
        :rtype: model_response
        """
        return self._request('GET', url, model_response, params=params, **kwargs)

    def delete(self, url, model_response=None, /, params=None, **kwargs):
        """
        :param url: str or furl
        :param model_response: (optional) sub class Union[BaseAPI, BasePydantic]
        :param params: (optional) List or Dictionary or bytes to be sent in the query
        :param kwargs: Optional arguments that ``_request`` takes.
        :rtype: model_response
        """
        return self._request('DELETE', url, model_response, params=params, **kwargs)

    def post(self, url, model_response=None, /, params=None, data=None, byte=False, **kwargs):
        """
        :param url: str or furl
        :param model_response: (optional) sub class Union[BaseAPI, BasePydantic]
        :param params: (optional) List or Dictionary or bytes to be sent in the query
        :param data: Dictionary, list of tuples, bytes, file-like, or subclass Union[BaseAPI, BasePydantic]
        :param byte: return byte response
        :param path: save file path
        :param kwargs: Optional arguments that ``_request`` takes.
        :rtype: model_response
        """
        return self._request('POST', url, model_response, params=params, data=data, byte=byte, **kwargs)

    def put(self, url, model_response=None, /, params=None, byte=False, **kwargs):
        """
        :param url: str or furl
        :param model_response: (optional) sub class Union[BaseAPI, BasePydantic]
        :param params: (optional) List or Dictionary or bytes to be sent in the query
        :param byte: return byte response
        :param path: save file path
        :param kwargs: Optional arguments that ``_request`` takes.
        :rtype: model_response
        """
        return self._request('PUT', url, model_response, params=params, byte=byte, **kwargs)

    def patch(self, url, model_response=None, /, params=None, **kwargs):
        """
        :param url: str or furl
        :param model_response: (optional) sub class Union[BaseAPI, BasePydantic]
        :param params: (optional) List or Dictionary or bytes to be sent in the query
        :param kwargs: Optional arguments that ``_request`` takes.
        :rtype: model_response
        """
        return self._request('PATCH', url, model_response, params=params, **kwargs)
