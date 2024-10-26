from pydantic import Field

from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotOrder
from odyssey_exchange_api.requests.base import SignedRequest


class SpotQueryOrderRequest(SignedRequest[SpotOrder]):
    """
    Get the order data. Returns a :class:`odyssey_exchange_api.objects.SpotOrder`.
    """
    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/order"

    __returning__ = SpotOrder

    order_id: str = Field(serialization_alias="orderId")
    """Order ID."""
    symbol: str
    """The lowercase symbol name, e.g., btcusdt."""
