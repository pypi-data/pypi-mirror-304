from decimal import Decimal

from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.enums import SpotOrderSide, SpotOrderType
from odyssey_exchange_api.requests.base import SignedRequest


class SpotTestCreateOrderRequest(SignedRequest[dict]):
    """
    Create a new test order. Returns an empty :class:`dict`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/spot-trading-api#test-new-order
    """

    _request_url = BASE_SPOT_URL
    _request_method = "POST"
    _request_path = "/sapi/v1/order/test"

    __returning__ = dict

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    volume: Decimal
    """Order quantity, there is a precision limit."""
    side: SpotOrderSide
    """Order side, BUY or SELL."""
    type: SpotOrderType
    """Order type, LIMIT or MARKET."""

    price: Decimal | None = None
    """Order price, for LIMIT orders must be sent, there is a precision limit."""
    newClientOrderId: str | None = None
    """Client order ID."""
