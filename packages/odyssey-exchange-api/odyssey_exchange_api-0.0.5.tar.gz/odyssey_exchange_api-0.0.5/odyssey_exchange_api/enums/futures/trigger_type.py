from enum import Enum


class FuturesTriggerType(int, Enum):
    STOP_LOSS = 1
    TAKE_PROFIT = 2
    STOP_LOSS_LIMIT = 3
    TAKE_PROFIT_LIMIT = 4
