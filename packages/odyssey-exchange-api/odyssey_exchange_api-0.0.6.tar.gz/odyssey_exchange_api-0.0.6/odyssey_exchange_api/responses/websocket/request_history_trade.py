from .base import WebsocketResponse
from ...objects import WebsocketHistoryTrade


class WebsocketHistoryTradeResponse(WebsocketResponse):
    __resolve_pattern__ = r"^market_\w+_trade_ticker$"

    event_rep: str
    channel: str
    ts: int
    status: str
    data: list[WebsocketHistoryTrade]
