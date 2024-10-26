from enum import Enum


class FuturesContractStatus(int, Enum):
    NOT_TRADABLE = 0
    TRADABLE = 1
