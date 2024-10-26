from pydantic import BaseModel

from .base import WebsocketResponse
from ...objects import WebsocketHistoryTrade


class WebsocketRealTimeTradeTickData(BaseModel):
    data: list[WebsocketHistoryTrade]
    ts: int


class WebsocketRealTimeTradeResponse(WebsocketResponse):
    __resolve_pattern__ = r"^market_\w+_trade_ticker$"

    channel: str
    ts: int
    tick: WebsocketRealTimeTradeTickData
    data: None
    status: str
