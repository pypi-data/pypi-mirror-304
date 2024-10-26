import json
import time
from typing import NoReturn

from httpx import AsyncClient
from websockets.asyncio.client import connect

from odyssey_exchange_api.requests.base import BaseRequest, SignedRequest, ResponseType, WebsocketRequest
from .client import OdysseyExchangeAPI
from ..base import BASE_WEBSOCKET_URL
from ..responses import WebsocketResponse


class AsyncOdysseyExchangeAPI(OdysseyExchangeAPI):
    def __init__(
            self, api_key: str,
            secret_key: str,
            client_parameters: dict = None
    ):
        """
        Class for asynchronous work with API.

        :param api_key: your API key
        :param secret_key: your secret key
        :param client_parameters: optional dict with parameters to httpx.Client
        """

        super().__init__(api_key, secret_key)

        if client_parameters is None:
            client_parameters = {}

        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__client = AsyncClient(**client_parameters)

    async def init_websocket_connection(self) -> NoReturn:
        self.__websocket_client = await connect(BASE_WEBSOCKET_URL)

    async def make_request(self, api_request: BaseRequest[ResponseType]) -> ResponseType:
        """
        Makes a asynchronous call to the api

        :param api_request: any of API requests which inherits from :class:`BaseRequest`.
        :return: an object specified at API request
        """

        if isinstance(api_request, SignedRequest):
            timestamp = str(int(time.time()) * 1000)
            api_request.sign(
                timestamp=timestamp,
                api_key=self.__api_key,
                secret_key=self.__secret_key
            )

        request = api_request.build_request()
        response_obj = await self.__client.send(request=request)
        response = self.process_response(response_obj)
        return api_request.make_response(response)

    async def make_websocket_request(self, api_request: WebsocketRequest):
        """
        Makes asynchronous call to the websocket connection

        :param api_request: any of API requests which inherits from :class:`WebsocketRequest`.
        :return:
        """
        data = api_request.build_request_data()
        if not isinstance(data, str) and not isinstance(data, bytes):
            data = json.dumps(data)

        await self.__websocket_client.send(data)

    async def receive_websocket_message(self) -> WebsocketResponse:
        """
        Get a message from a websocket

        :return:
        """
        message = await self.__websocket_client.recv()
        response = self.process_websocket_message(message)
        return response
