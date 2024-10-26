import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class WebsocketKlineData(BaseModel):
    """
    An object that contains information about the kline data.
    """

    id: int
    """Open time"""
    open: Decimal
    """Open price"""
    close: Decimal
    """Close price"""
    high: Decimal
    """Highest price"""
    low: Decimal
    """Lowest price"""
    vol: Decimal
    """Trade volume"""
    amount: Decimal
    """Trade amount"""
    ds: datetime.datetime
    """Trade date"""
    trade_id: int = Field(validation_alias="tradeId")
    """Trade ID"""
