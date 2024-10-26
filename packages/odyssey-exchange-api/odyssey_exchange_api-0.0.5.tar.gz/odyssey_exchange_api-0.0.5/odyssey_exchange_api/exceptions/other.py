from .base import BaseExchangeException


class OrderNotExistException(BaseExchangeException):
    code = -2013
    msg = "订单不存在"
    reason = "Order does not exist."


class IncorrectAPIOrIPException(BaseExchangeException):
    code = -2015
    msg = "Invalid API key, IP or operation permission"
    reason = "Signature or IP is incorrect"


class FrozenTransactionsException(BaseExchangeException):
    code = -2016
    msg = "Transactions are frozen"
    reason = "The user's transaction is frozen"


class InsufficientBalanceException(BaseExchangeException):
    code = -2017
    msg = "余额不足"
    reason = "Insufficient balance"


class WrongParameterException(BaseExchangeException):
    code = -2100
    msg = "Parameter error"
    reason = "Input wrong parameter or exist block in the parameter"


class IllegalIPException(BaseExchangeException):
    code = -2200
    msg = "Illegal IP"
    reason = "Not trusted IP"


class RestrictedTransactionsException(BaseExchangeException):
    code = 35
    msg = "禁止下单(Forbidden to order)"
    reason = "User transactions may be restricted"
