from .base import WebsocketResponse
from ...objects import WebsocketTickerData


class WebsocketTickerResponse(WebsocketResponse):
    __resolve_pattern__ = r'^market_\w+_ticker$'

    event_rep: str
    channel: str
    data: None
    tick: WebsocketTickerData
    status: str
