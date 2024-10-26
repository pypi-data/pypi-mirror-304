from enum import Enum


class SpotOrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    buy = "buy"
    sell = "sell"
