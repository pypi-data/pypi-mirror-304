from enum import Enum


class FuturesOrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
