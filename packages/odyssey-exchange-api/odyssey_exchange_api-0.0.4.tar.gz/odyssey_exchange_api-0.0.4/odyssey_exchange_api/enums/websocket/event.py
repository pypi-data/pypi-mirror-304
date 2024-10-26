from enum import Enum


class WebsocketEventType(str, Enum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
