from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from odyssey_exchange_api.enums import SpotOrderStatus, SpotOrderType, SpotOrderSide


class SpotOrder(BaseModel):
    """
    An object that contains information about the order.
    """

    order_id: str = Field(alias="orderId")
    """Order ID"""
    client_order_id: str | None = Field(default=None, alias="clientOrderId")
    """User order ID"""
    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    transact_time: int | None = Field(default=None, alias="transactTime")
    """The time of place order"""
    price: Decimal
    """Order price"""
    original_quantity: Decimal = Field(alias="origQty")
    """Order volume"""
    executed_quantity: Decimal = Field(alias="executedQty")
    """The number of already deal order"""
    average_price: Decimal | None = Field(alias="avgPrice", default=None)
    """The average price of already deal order"""
    type: SpotOrderType
    """Type of the order"""
    side: SpotOrderSide
    """Side of the order"""
    status: SpotOrderStatus
    """Order status"""

    @field_validator("order_id", mode="before")
    @classmethod
    def retrieve_order_id(cls, v: str | list[str] | int) -> str:
        if isinstance(v, list):
            return v[0]
        return str(v)
