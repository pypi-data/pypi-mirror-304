from enum import Enum


class SpotOrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
