from .base import WebsocketResponse
from ...objects import WebsocketFullDepth


class WebsocketFullDepthResponse(WebsocketResponse):
    __resolve_pattern__ = r"^market_\w+_depth_step\d+$"

    channel: str
    ts: int
    tick: WebsocketFullDepth
    status: str
