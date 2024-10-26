import hashlib
import hmac
import urllib.parse
from typing import TypeVar, Any, Generic

from httpx import Request
from pydantic import BaseModel, TypeAdapter

ResponseType = TypeVar("ResponseType", bound=Any)
RequestDataType = TypeVar("RequestDataType", bound=Any)


class BaseRequest(BaseModel, Generic[ResponseType]):
    _request_url: str
    _request_method: str
    _request_path: str
    _request_headers = {}

    __returning__ = ResponseType

    def get_data(self):
        return self.model_dump(exclude_none=True, by_alias=True)

    def get_json(self):
        return self.model_dump_json(exclude_none=True, by_alias=True)

    def build_request(self) -> Request:
        data = None
        params = None

        if self._request_method == "GET":
            params = self.get_data()
        elif self._request_method == "POST":
            data = self.get_json()

        request = Request(
            method=self._request_method,
            url=self._request_url + self._request_path,
            headers=self._request_headers,
            data=data,
            params=params
        )
        return request

    def make_response(self, data) -> ResponseType:
        adapter = TypeAdapter(self.__returning__)
        response = adapter.validate_python(data)
        return response


class SignedRequest(BaseRequest[ResponseType]):
    def sign(
            self,
            timestamp: str,
            api_key: str,
            secret_key: str
    ):
        if self._request_method == "GET":
            data = self.get_data()
            data = urllib.parse.urlencode(data)
            data = "?" + data if data else ""
        else:
            data = self.get_json()

        _raw_sign = f"{timestamp}{self._request_method}{self._request_path}{data}"

        m = hmac.new(secret_key.encode("utf-8"), _raw_sign.encode('utf-8'), hashlib.sha256)
        sign = m.hexdigest()

        self._request_headers["X-CH-APIKEY"] = api_key
        self._request_headers["X-CH-SIGN"] = sign
        self._request_headers["X-CH-TS"] = timestamp
        self._request_headers["Content-Type"] = "application/json"


class WebsocketRequest(BaseModel):
    def get_data(self):
        return self.model_dump(exclude_none=True, by_alias=True)

    def get_json(self):
        return self.model_dump_json(exclude_none=True, by_alias=True)

    def build_request_data(self) -> dict:
        return self.get_data()
