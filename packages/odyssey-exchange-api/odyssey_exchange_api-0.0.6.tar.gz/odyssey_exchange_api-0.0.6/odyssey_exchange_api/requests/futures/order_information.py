from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesOrder
from odyssey_exchange_api.requests.base import SignedRequest


class FuturesOrderInfoRequest(SignedRequest[FuturesOrder]):
    """
    Get the order data. Returns a :class:`odyssey_exchange_api.objects.FuturesOrder`.
    """
    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/order"

    __returning__ = FuturesOrder

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    order_id: str = Field(serialization_alias="orderId")
    """Order ID."""
    client_order_id: str | None = Field(serialization_alias="clientOrderId", default=None)
    """Client order ID."""
