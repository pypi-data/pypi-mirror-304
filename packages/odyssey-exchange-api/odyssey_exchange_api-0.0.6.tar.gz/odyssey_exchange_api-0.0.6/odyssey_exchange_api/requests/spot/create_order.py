from decimal import Decimal

from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.enums import SpotOrderSide, SpotOrderType
from odyssey_exchange_api.objects import SpotOrder
from odyssey_exchange_api.requests.base import SignedRequest


class SpotCreateOrderRequest(SignedRequest[SpotOrder]):
    """
    Create a new order. Returns a :class:`odyssey_exchange_api.objects.SpotOrder`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "POST"
    _request_path = "/sapi/v1/order"

    __returning__ = SpotOrder

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    volume: Decimal
    """Order quantity, there is a precision limit."""
    side: SpotOrderSide
    """Order side."""
    type: SpotOrderType
    """Order type."""

    price: Decimal | None = None
    """Order price, for LIMIT orders must be sent, there is a precision limit."""
    newClientOrderId: str | None = None
    """Client order ID."""
