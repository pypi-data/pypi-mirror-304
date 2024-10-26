from decimal import Decimal

from pydantic import BaseModel


class FuturesDepthResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.FuturesDepthRequest`.

    Contains an arrays with price and volume.
    """

    asks: list[list[Decimal]]
    """Order book selling information, the array length is 2, subscript one is the price, type is float; subscript two is the quantity corresponding to the current price, type is float"""
    bids: list[list[Decimal]]
    """Order book buying information, the array length is 2, subscript one is the price, type is float; subscript two is the quantity corresponding to the current price, type is float"""
    time: int | None
    """Current timestamp, nullable"""
