from .base import BaseExchangeException


class RateLimitException(BaseExchangeException):
    msg = "You have reached the rate limit"
