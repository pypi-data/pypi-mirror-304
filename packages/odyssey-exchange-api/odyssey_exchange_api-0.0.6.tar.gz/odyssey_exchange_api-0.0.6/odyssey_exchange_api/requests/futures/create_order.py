from decimal import Decimal

from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.enums import FuturesOrderSide, FuturesOrderType, FuturesPositionSide, FuturesPositionType, \
    FuturesTimeInForce
from odyssey_exchange_api.requests.base import SignedRequest
from odyssey_exchange_api.responses import FuturesOrderIDResponse


class FuturesCreateOrderRequest(SignedRequest[FuturesOrderIDResponse]):
    """
    Create a new order. Returns a :class:`odyssey_exchange_api.responses.FuturesOrderIDResponse`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/order"

    __returning__ = FuturesOrderIDResponse

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    volume: Decimal
    """The number of orders placed has a precision limit. When opening a position at market price, the unit here is value."""
    side: FuturesOrderSide
    """Order side."""
    type: FuturesOrderType
    """Order type."""
    open: FuturesPositionSide
    """Position side."""
    position_type: FuturesPositionType = Field(serialization_alias="positionType")
    """Position type."""

    price: Decimal | None = None
    """Order price, for LIMIT orders must be sent, there is a precision limit."""
    clientOrderId: str | None = None
    """Client order ID."""
    timeInForce: FuturesTimeInForce | None = None
    """Time in force is a special instruction that indicates how long an order will remain active until it is executed or expires."""
