from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import SignedRequest, ResponseType


class FuturesCancelTriggerOrderRequest(SignedRequest[bool]):
    """
    Cancel trigger order. Returns a :class:`bool`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/v1/inner/trigger_order_cancel"

    __returning__ = bool

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    order_id: str = Field(serialization_alias="orderId")
    """Order ID."""

    def make_response(self, data) -> ResponseType:
        if data.get("code") == "0" and data.get("msg") == "成功":
            return True
        return False
