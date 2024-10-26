from odyssey_exchange_api.requests.base import WebsocketRequest


class WebsocketPongRequest(WebsocketRequest):
    """
    PONG is the response to the PING request.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/websocket#heartbeat
    """
    pong: int
