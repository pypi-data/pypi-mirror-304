from .base import BaseExchangeException


class UnknownExchangeException(BaseExchangeException):
    code = -1000
    msg = "An unknown error occurred while processing the request"
    reason = "The wrong input parameter symbol name or input wrong contract name."


class DisconnectedException(BaseExchangeException):
    code = -1001
    msg = "内部错误; 无法处理您的请求。 请再试一次"
    reason = "Internal error; unable to process your request. Please try again."


class MissingAPIKeyException(BaseExchangeException):
    code = -1002
    msg = ("You are not authorized to execute this request. "
           "The request needs to send an API Key, and we recommend appending the X-CH-APIKEY to all request headers")
    reason = "The X_CH_APIKEY required for signature is not added to the header."


class TooManyRequestsException(BaseExchangeException):
    code = -1003
    msg = "请求过于频繁超过限制"
    reason = "Requests exceed the limit too frequently."


class NoThisCompanyException(BaseExchangeException):
    code = -1004
    msg = "您无权执行此请求 user not exit"
    reason = "You are not authorized to execute this request. User not exit Company."


class UnexpectedResponseException(BaseExchangeException):
    code = -1006
    msg = "接收到了不符合预设格式的消息，下单状态未知"
    reason = ("An unexpected response was received from the message bus. Execution status unknown. "
              "OPEN API server find some exception in execute request. Please report to Customer service.")


class TimeoutAPIException(BaseExchangeException):
    code = -1007
    msg = "等待后端服务器响应超时。 发送状态未知； 执行状态未知"
    reason = "Timeout waiting for response from backend server. Send status unknown; execution status unknown."


class UnknownOrderCompositionException(BaseExchangeException):
    code = -1014
    msg = "不支持的订单组合"
    reason = "Unsupported order combination."


class TooManyOrdersException(BaseExchangeException):
    code = -1015
    msg = "Too many orders. Please reduce the number of your orders"
    reason = "The order quantity exceeds the maximum quantity limit."


class ServiceShuttingDownException(BaseExchangeException):
    code = -1016
    msg = "服务器下线"
    reason = "This service is no longer available."


class NoContentTypeException(BaseExchangeException):
    code = -1017
    msg = "我们建议在所有的请求头附加Content-Type, 并设置成application/json"
    reason = "We recommend attaching Content-Type to all request headers and setting it to application/json."


class UnsupportedOperationException(BaseExchangeException):
    code = -1020
    msg = "不支持此操作"
    reason = "This operation is not supported."


class InvalidTimestampException(BaseExchangeException):
    code = -1021
    msg = "Invalid timestamp with too large time offset"
    reason = ("The timestamp offset is too large. Timestamp for this request was 1000ms ahead of the server's time. "
              "Please check the difference between your local time and server time.")


class InvalidSignatureException(BaseExchangeException):
    code = -1022
    msg = "Invalid signature"
    reason = "Signature verification failed"


class MissingTimestampException(BaseExchangeException):
    code = -1023
    msg = ("You are not authorized to execute this request. "
           "The request need to send timestamps, and we recommend appending X-CH-TS to all request headers")
    reason = "The X-CH-TS required for signature is not added to the header."


class MissingSignatureException(BaseExchangeException):
    code = -1024
    msg = ("You are not authorized to execute this request. "
           "The request needs to send sign, and we recommend appending X-CH-SIGN to all request headers")
    reason = "The X-CH-SIGN required for signature is not added to the header."
