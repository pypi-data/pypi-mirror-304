from enum import Enum


class FuturesContractType(str, Enum):
    PERPETUAL = "E"
    SIMULATED = "S"
