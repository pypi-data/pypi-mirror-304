from odyssey_exchange_api.exceptions.base import BaseExchangeException, UnknownException
from odyssey_exchange_api.exceptions.rate_limit import RateLimitException
from odyssey_exchange_api.exceptions.general import DisconnectedException, UnknownExchangeException, \
    UnknownOrderCompositionException, \
    TooManyOrdersException, TooManyRequestsException, TimeoutAPIException, MissingAPIKeyException, \
    MissingSignatureException, MissingTimestampException, InvalidSignatureException, InvalidTimestampException, \
    UnexpectedResponseException, UnsupportedOperationException, NoThisCompanyException, \
    NoContentTypeException, ServiceShuttingDownException
from odyssey_exchange_api.exceptions.other import RestrictedTransactionsException, FrozenTransactionsException, \
    IllegalIPException, \
    WrongParameterException, InsufficientBalanceException, OrderNotExistException, IncorrectAPIOrIPException
from odyssey_exchange_api.exceptions.request import InvalidContractException, InvalidSideException, \
    InvalidSpotOrderTypeException, \
    NoPendingOrdersException, OrderPriceRangeException, NotCancellableOrderException, NotRequiredParamException, \
    UnknownParamException, RequiredParamException, RequiredParamEmptyException, UnreadParamException, \
    OrderMaximumLimitException, OrderVolumeNotEnoughException, BadPrecisionException, IllegalCharsException, \
    TooManyParametersException, MarketTradingDisabledException

EXCEPTIONS_DICT = {
    -1001: DisconnectedException,
    -1000: UnknownExchangeException,
    -1014: UnknownOrderCompositionException,
    -1015: TooManyOrdersException,
    -1003: TooManyRequestsException,
    -1007: TimeoutAPIException,
    -1002: MissingAPIKeyException,
    -1024: MissingSignatureException,
    -1023: MissingTimestampException,
    -1022: InvalidSignatureException,
    -1021: InvalidTimestampException,
    -1006: UnexpectedResponseException,
    -1020: UnsupportedOperationException,
    -1004: NoThisCompanyException,
    -1017: NoContentTypeException,
    -1016: ServiceShuttingDownException,
    -1121: InvalidContractException,
    -1117: InvalidSideException,
    -1116: InvalidSpotOrderTypeException,
    -1112: NoPendingOrdersException,
    -1138: OrderPriceRangeException,
    -1145: NotCancellableOrderException,
    -1106: NotRequiredParamException,
    -1103: UnknownParamException,
    -1102: RequiredParamException,
    -1105: RequiredParamEmptyException,
    -1104: UnreadParamException,
    -1147: OrderMaximumLimitException,
    -1136: OrderVolumeNotEnoughException,
    -1111: BadPrecisionException,
    -1100: IllegalCharsException,
    -1101: TooManyParametersException,
    -1139: MarketTradingDisabledException,
    35: RestrictedTransactionsException,
    -2016: FrozenTransactionsException,
    -2200: IllegalIPException,
    -2100: WrongParameterException,
    -2017: InsufficientBalanceException,
    -2013: OrderNotExistException,
    -2015: IncorrectAPIOrIPException,
}
