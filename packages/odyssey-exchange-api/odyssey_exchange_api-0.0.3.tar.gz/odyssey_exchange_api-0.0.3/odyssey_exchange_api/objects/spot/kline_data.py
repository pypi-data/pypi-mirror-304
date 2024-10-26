from decimal import Decimal

from pydantic import BaseModel


class SpotKlineData(BaseModel):
    """
    An object that contains information about the kline data.
    """

    idx: int
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
