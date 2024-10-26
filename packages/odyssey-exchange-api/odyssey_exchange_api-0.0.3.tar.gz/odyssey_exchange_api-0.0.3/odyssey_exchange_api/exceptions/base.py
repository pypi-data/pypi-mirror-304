from typing import Any


class UnknownException(Exception):
    pass


class BaseExchangeException(Exception):
    code: int
    msg: str
    reason: str
    data: Any

    def __init__(self, data: Any = None):
        super().__init__(self.msg)
        self.data = data
