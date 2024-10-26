from decimal import Decimal

from pydantic import BaseModel


class FuturesTickerData(BaseModel):
    """
    An object with information about a contract per day.
    """

    time: int
    """Timestamp"""
    high: Decimal
    """Highest price"""
    low: Decimal
    """Lowest price"""
    last: Decimal
    """Latest deal price"""
    vol: Decimal
    """Trade volume"""
    buy: Decimal
    """The price in the buying book order at the first one"""
    sell: Decimal
    """The price in the selling book order at the first one"""
    rose: str
    """Range of increase and decrease, + is increase, - is decrease, +0.05 means increase by 5%"""
