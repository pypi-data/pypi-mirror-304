from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import SpotOrderSide, SpotOrderType


class SpotSingleBatchOrder(BaseModel):
    """
    An object with information about a single order in batch orders.
    """

    volume: Decimal
    """Order volume"""
    side: SpotOrderSide
    """Order side"""
    batch_type: SpotOrderType = Field(serialization_alias="batchType")
    """Order type"""

    price: Decimal | None = None
    """Order price"""
