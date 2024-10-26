from .base import WebsocketResponse


class WebsocketPingResponse(WebsocketResponse):
    ping: int
