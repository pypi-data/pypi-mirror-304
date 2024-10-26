from decimal import Decimal

from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.enums import FuturesOrderSide, FuturesOrderType, FuturesPositionSide, FuturesPositionType, \
    FuturesTriggerType
from odyssey_exchange_api.requests.base import SignedRequest, ResponseType
from odyssey_exchange_api.responses import FuturesCreateConditionOrderResponse


class FuturesCreateConditionOrderRequest(SignedRequest[FuturesCreateConditionOrderResponse]):
    """
    Create a new condition order. Returns a :class:`odyssey_exchange_api.responses.FuturesCreateConditionOrderResponse`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/conditionOrder"

    __returning__ = FuturesCreateConditionOrderResponse

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    trigger_type: FuturesTriggerType = Field(serialization_alias="triggerType")
    """Type of condition."""
    trigger_price: Decimal = Field(serialization_alias="triggerPrice")
    """Trigger price."""
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

    def make_response(self, data) -> ResponseType:
        return super().make_response(data["data"])
