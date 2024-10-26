from pydantic import BaseModel, field_validator, Field

from odyssey_exchange_api.enums import SpotOrderStatus


class SpotCancelOrderResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.SpotCancelOrderRequest`.

    Contains an order id, asset symbol and order status.
    """

    order_id: str = Field(alias="orderId")
    """Order ID"""
    symbol: str
    """The lowercase symbol name, e.g., btcusdt."""
    status: SpotOrderStatus
    """Order status"""

    @field_validator("order_id", mode="before")
    @classmethod
    def retrieve_order_id(cls, v: str | list[str]) -> str:
        if isinstance(v, list):
            return v[0]
        return v
