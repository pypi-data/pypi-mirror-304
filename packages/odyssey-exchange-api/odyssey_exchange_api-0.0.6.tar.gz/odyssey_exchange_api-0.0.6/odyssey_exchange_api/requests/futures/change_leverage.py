from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import SignedRequest, ResponseType


class FuturesChangeLeverageRequest(SignedRequest[bool]):
    """
    Change leverage. Returns a :class:`odyssey_exchange_api.responses.FuturesAccountInfoResponse`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/edit_lever"

    __returning__ = bool

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    now_level: int = Field(serialization_alias="nowLevel")
    """Leverage multiple to be modified."""

    def make_response(self, data) -> ResponseType:
        if data.get("code") == "0" and data.get("msg") == "成功":
            return True
        return False
