from .base import WebsocketResponse
from ...objects import WebsocketKlineData


class WebsocketKlineResponse(WebsocketResponse):
    __resolve_pattern__ = r'^market_\w+_kline_\w+$'

    channel: str
    ts: int
    data: list[WebsocketKlineData] | None
    tick: WebsocketKlineData | None
    status: str
