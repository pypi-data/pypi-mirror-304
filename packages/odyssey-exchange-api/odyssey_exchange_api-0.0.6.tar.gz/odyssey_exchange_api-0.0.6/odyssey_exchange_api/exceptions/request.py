from .base import BaseExchangeException


class IllegalCharsException(BaseExchangeException):
    code = -1100
    msg = "请求中存在非法字符"
    reason = "Illegal characters found in a parameter."


class TooManyParametersException(BaseExchangeException):
    code = -1101
    msg = "发送的参数太多"
    reason = "Too many parameters sent for this endpoint."


class RequiredParamException(BaseExchangeException):
    code = -1102
    msg = "Forced parameter XXX not sent, empty or incorrect format"
    reason = "The parameter is null, the required parameter not input or incorrect format of input parameters"


class UnknownParamException(BaseExchangeException):
    code = -1103
    msg = "发送了未知参数"
    reason = "Each request requires at least one parameter"


class UnreadParamException(BaseExchangeException):
    code = -1104
    msg = "并非所有发送的参数都被读取"
    reason = "Not all sent parameters were read; read '%s' parameter(s) but was sent '%s'."


class RequiredParamEmptyException(BaseExchangeException):
    code = -1105
    msg = "The parameter XXX is empty"
    reason = "The required parameter is empty"


class NotRequiredParamException(BaseExchangeException):
    code = -1106
    msg = "不需要发送此参数"
    reason = "Parameter '%s' sent when not required."


class BadPrecisionException(BaseExchangeException):
    code = -1111
    msg = "精度超过此资产定义的最大值"
    reason = "Precision is over the maximum defined for this asset."


class NoPendingOrdersException(BaseExchangeException):
    code = -1112
    msg = "There are no pending orders for trading pairs"
    reason = "The order that needs to be canceled does not exist."


class InvalidSpotOrderTypeException(BaseExchangeException):
    code = -1116
    msg = "Invalid order type"
    reason = "Invalid orderType. In the current version , ORDER_TYPE values is LIMIT or MARKET."


class InvalidSideException(BaseExchangeException):
    code = -1117
    msg = "Invalid buying or selling direction"
    reason = "Invalid side. ORDER_SIDE values is BUY or SELL"


class InvalidContractException(BaseExchangeException):
    code = -1121
    msg = "Invalid contract"
    reason = "Invalid symbol."


class OrderVolumeNotEnoughException(BaseExchangeException):
    code = -1136
    msg = "订单数量小于最小值"
    reason = "Order volume lower than the minimum."


class OrderPriceRangeException(BaseExchangeException):
    code = -1138
    msg = "The order price is outside the allowable range"
    reason = "Order price exceeds permissible range."


class MarketTradingDisabledException(BaseExchangeException):
    code = -1139
    msg = "The pair does not support market trading"
    reason = "This trading pair does not support market trading"


class NotCancellableOrderException(BaseExchangeException):
    code = -1145
    msg = "The order status does not allow for cancellation"
    reason = "The order cannot be canceled"


class OrderMaximumLimitException(BaseExchangeException):
    code = -1147
    msg = "价格或数量精度超过最大限制"
    reason = "Order price or quantity exceeds the maximum limit"
