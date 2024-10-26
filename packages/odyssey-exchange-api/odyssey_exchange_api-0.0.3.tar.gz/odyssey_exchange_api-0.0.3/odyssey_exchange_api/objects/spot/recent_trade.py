from decimal import Decimal

from pydantic import BaseModel

from odyssey_exchange_api.enums import SpotOrderSide


class SpotRecentTrade(BaseModel):
    """
    An object that contains information about recent trades.
    """

    side: SpotOrderSide
    """Order side"""
    price: Decimal
    """Trade price"""
    qty: Decimal
    """The quantity traded"""
    time: int
    """Trade timestamp"""
