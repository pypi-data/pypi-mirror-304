import datetime
from decimal import Decimal

from pydantic import BaseModel

from odyssey_exchange_api.enums import WebsocketOrderSide


class WebsocketHistoryTrade(BaseModel):
    """
    An object that contains information about history trades.
    """

    side: WebsocketOrderSide
    """Order side"""
    price: Decimal
    """Trade price"""
    amount: Decimal
    """The volume of the base coin"""
    vol: Decimal
    """the volume of the main coin"""
    ts: int
    """Trade timestamp"""
    ds: datetime.datetime
    """Trade date"""
