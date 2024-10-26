from decimal import Decimal

from pydantic import BaseModel


class WebsocketTickerData(BaseModel):
    """
    An object with information about an asset per day.
    """

    high: Decimal
    """Highest price"""
    low: Decimal
    """Lowest price"""
    vol: Decimal
    """Trade volume"""
    amount: Decimal
    """Trade amount"""
    rose: str
    """Range of increase and decrease, + is increase, - is decrease, +0.05 means increase by 5%"""
