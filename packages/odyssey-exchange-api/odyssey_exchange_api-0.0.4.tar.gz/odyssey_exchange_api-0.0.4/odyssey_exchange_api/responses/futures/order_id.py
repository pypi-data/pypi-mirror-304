from pydantic import BaseModel, Field


class FuturesOrderIDResponse(BaseModel):
    """
    Contains an object with order id.
    """

    order_id: int = Field(alias="orderId")
    """Order ID"""
