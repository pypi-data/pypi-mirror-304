from enum import Enum


class WebsocketOrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
