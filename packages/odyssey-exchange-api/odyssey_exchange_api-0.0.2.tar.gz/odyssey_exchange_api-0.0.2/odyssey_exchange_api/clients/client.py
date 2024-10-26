import json
import zlib
from typing import Any, NoReturn

from httpx import Response

from odyssey_exchange_api.exceptions import UnknownException, EXCEPTIONS_DICT
from odyssey_exchange_api.requests.base import BaseRequest, ResponseType
from odyssey_exchange_api.responses import WebsocketResponse
from odyssey_exchange_api.utils import resolve_websocket_response_class


class OdysseyExchangeAPI:
    def __init__(
            self,
            api_key: str,
            secret_key: str,
    ):
        """
        The base class of the API client, use it to inherit your own clients.

        :param api_key: your API key
        :param secret_key: your secret key
        """

        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__websocket_client = None

    def process_response(self, response: Response) -> Any:
        """
        Checks the response from the api, if there is an error raises the error, if not returns data from the response

        :param response: :class:`httpx.Response`
        :return: any
        """
        try:
            response_data = response.json()
        except:
            raise UnknownException(response.content)

        if not isinstance(response_data, dict):
            return response_data

        code = response_data.get("code")
        if code and code != '0':
            exc_class = EXCEPTIONS_DICT.get(int(code))
            if not exc_class:
                raise UnknownException(response_data)

            data = response_data.get("data")
            raise exc_class(data)
        else:
            if 200 < response.status_code < 300:
                raise UnknownException(response_data)
            return response_data

    def process_websocket_message(self, message: bytes) -> WebsocketResponse:
        decoded_message = zlib.decompress(message, 16 + zlib.MAX_WBITS)
        data = json.loads(decoded_message)
        response_obj = resolve_websocket_response_class(data)
        return response_obj(**data)

    def init_websocket_connection(self) -> NoReturn:
        """
        Initialize the websocket client for further work with the websocket API.
        """
        raise NotImplementedError

    def make_request(self, api_request: BaseRequest[ResponseType]) -> ResponseType:
        """
        Makes a call to the api

        :param api_request: any of API requests which inherits from :class:`BaseRequest`.
        :return: an object specified at API request
        """
        raise NotImplementedError
