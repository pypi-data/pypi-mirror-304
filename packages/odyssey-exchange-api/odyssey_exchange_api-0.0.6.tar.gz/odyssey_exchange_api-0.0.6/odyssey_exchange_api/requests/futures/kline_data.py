from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesKlineData
from odyssey_exchange_api.requests.base import BaseRequest


class FuturesKlineDataRequest(BaseRequest[list[FuturesKlineData]]):
    """
    Retrieve Kline/candlestick data. Returns an array of :class:`FuturesKlineData`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/klines"

    __returning__ = list[FuturesKlineData]

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    interval: str
    """Interval of the Kline. Possible values include: 1min, 5min, 15min, 30min, 60min, 1day, 1week, 1month."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 300."""
