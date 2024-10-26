from enum import Enum


class FuturesPositionSide(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
