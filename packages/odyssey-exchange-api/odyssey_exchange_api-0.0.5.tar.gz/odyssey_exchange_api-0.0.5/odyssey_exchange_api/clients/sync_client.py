import json
import time
from typing import NoReturn

from httpx import Client
from websockets.sync.client import connect

from odyssey_exchange_api.requests.base import BaseRequest, SignedRequest, ResponseType, WebsocketRequest
from .client import OdysseyExchangeAPI
from ..base import BASE_WEBSOCKET_URL
from ..responses import WebsocketResponse


class SyncOdysseyExchangeAPI(OdysseyExchangeAPI):
    def __init__(
            self, api_key: str,
            secret_key: str,
            client_parameters: dict = None
    ):
        """
        Class for synchronous work with API.

        :param api_key: your API key
        :param secret_key: your secret key
        :param client_parameters: optional dict with parameters to httpx.Client
        """

        super().__init__(api_key, secret_key)

        if client_parameters is None:
            client_parameters = {}

        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__client = Client(**client_parameters)

    def init_websocket_connection(self) -> NoReturn:
        self.__websocket_client = connect(BASE_WEBSOCKET_URL)

    def make_request(self, api_request: BaseRequest[ResponseType]) -> ResponseType:
        """
        Makes a synchronous call to the api

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
        response_obj = self.__client.send(request=request)
        response = self.process_response(response_obj)
        return api_request.make_response(response)

    def make_websocket_request(self, api_request: WebsocketRequest):
        """
        Makes a synchronous call to the websocket connection

        :param api_request: any of API requests which inherits from :class:`WebsocketRequest`.
        :return:
        """
        data = api_request.build_request_data()
        if not isinstance(data, str) and not isinstance(data, bytes):
            data = json.dumps(data)
        self.__websocket_client.send(data)

    def receive_websocket_message(self, timeout: int = 5000) -> WebsocketResponse:
        """
        Get a message from a websocket

        :param timeout: milliseconds of waiting for a message from the websocket.
        :return:
        """
        message = self.__websocket_client.recv(timeout)
        response = self.process_websocket_message(message)
        return response
