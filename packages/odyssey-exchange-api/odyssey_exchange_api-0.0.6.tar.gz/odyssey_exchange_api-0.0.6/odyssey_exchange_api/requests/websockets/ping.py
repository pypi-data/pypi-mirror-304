from odyssey_exchange_api.requests.base import WebsocketRequest


class WebsocketPongRequest(WebsocketRequest):
    """
    PONG is the response to the PING request.
    """
    pong: int
