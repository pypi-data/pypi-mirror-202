from dataclasses import dataclass, field
from typing import Dict, Union

import allure
from aiohttp import ClientResponse, ClientSession

from .log_request import log_request
from .microservices import MicroservicesTemplate, prepare
from .model import BaseAPI, BasePydantic
from ..helpers import attach_json, dumps


class AsyncResponse(ClientResponse):
    @property
    def status_code(self):
        return self.status

    @property
    def elapsed(self):
        return 0

    @property
    def request(self):
        return self.request_info


class AsyncSession(ClientSession):
    def __init__(self, *args, response_class=AsyncResponse, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            response_class=response_class,
            json_serialize=dumps,
        )

    def __init_subclass__(cls, **kwargs):
        pass


@dataclass
class AsyncMicroservicesTemplate(MicroservicesTemplate):
    session: ClientSession = field(default_factory=AsyncSession)
    cookies: dict = field(default_factory=dict)

    def __post_init__(self):
        self.session.cookie_jar.update_cookies(self.cookies)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    # Tools #####################################
    async def _result(self, response):
        result = await response.json()
        assert result.get('code', 'ok') == 'ok'
        return result.get(self.json_data, result)

    async def _validation(self, response: ClientResponse, byte=False, text='', **kwargs) -> Union[Dict, bytes]:
        text = await response.text()
        super()._validation(response, byte, text, **kwargs)
        return await self._result(response)

    @prepare
    @log_request
    async def _request(
            self,
            method,
            url,
            model_response: Union[BaseAPI, BasePydantic] = None,
            params=None,
            data=None,
            json=None,
            headers=None,
            byte=False,
            **kwargs
    ):
        with allure.step(f'{method} {url}'):
            response = await self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                ssl=False,
                **kwargs
            )
            if data or json:
                attach_json(data or json, name='Request payload')

            with allure.step('Check response'):
                result = await self._validation(response, byte)
                if byte:
                    return result

            attach_json(result, name='Result')

        return model_response.init(result)

    async def get(self, url, model_response=None, /, params=None, **kwargs):
        """
        :rtype: model_response
        """
        return await self._request('GET', url, model_response, params=params, **kwargs)

    async def delete(self, url, model_response=None, /, params=None, data=None, headers=None):
        """
        :rtype: model_response
        """
        return await self._request('DELETE', url, model_response, params=params, data=data, headers=headers)

    async def post(self, url, model_response=None, /, params=None, data=None, json=None, headers=None, byte=False):
        """
        :rtype: model_response
        """
        return await self._request('POST', url, model_response, params=params, data=data, json=json, headers=headers,
                                   byte=byte)

    async def put(self, url, model_response=None, /, params=None, data=None, json=None, headers=None, byte=False):
        """
        :rtype: model_response
        """
        return await self._request('PUT', url, model_response, params=params, data=data, json=json, headers=headers)

    async def patch(self, url, model_response=None, /, params=None, data=None, json=None, headers=None):
        """
        :rtype: model_response
        """
        return await self._request('PATCH', url, model_response, params=params, data=data, json=json, headers=headers)
