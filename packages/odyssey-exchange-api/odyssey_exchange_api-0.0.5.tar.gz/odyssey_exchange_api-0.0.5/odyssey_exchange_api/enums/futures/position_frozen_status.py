from enum import Enum


class FuturesPositionFrozenStatus(int, Enum):
    NORMAL = 0
    LIQUIDATION_FROZEN = 1
    DELIVERY_FROZEN = 2
