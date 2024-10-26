import re
from typing import Type

from odyssey_exchange_api.responses import WebsocketHistoryTradeResponse, WebsocketResponse, \
    WebsocketKlineResponse, WebsocketTickerResponse, WebsocketRealTimeTradeResponse
from odyssey_exchange_api.responses.websocket import WebsocketPingResponse, WebsocketFullDepthResponse


def resolve_websocket_response_class(data: dict) -> Type[WebsocketResponse] | None:
    stream_responses_obj = [
        WebsocketFullDepthResponse,
        WebsocketKlineResponse,
        WebsocketRealTimeTradeResponse,
        WebsocketTickerResponse,
    ]

    request_responses_obj = [
        WebsocketHistoryTradeResponse,
        WebsocketKlineResponse,
    ]

    if data.get("ping"):
        return WebsocketPingResponse

    elif data.get("event_rep"):
        current_responses_list = request_responses_obj
    else:
        current_responses_list = stream_responses_obj

    for response_obj in current_responses_list:
        pattern = re.compile(response_obj.__resolve_pattern__)
        if pattern.match(data.get("channel")):
            return response_obj
