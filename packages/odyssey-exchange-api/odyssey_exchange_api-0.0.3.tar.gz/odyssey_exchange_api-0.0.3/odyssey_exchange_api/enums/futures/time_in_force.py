from enum import Enum


class FuturesTimeInForce(str, Enum):
    IOC = "IOC"
    FOK = "FOK"
    POST_ONLY = "POST_ONLY"
