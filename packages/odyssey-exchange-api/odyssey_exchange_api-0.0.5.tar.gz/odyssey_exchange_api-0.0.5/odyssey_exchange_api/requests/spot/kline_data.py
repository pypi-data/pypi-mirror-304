from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotKlineData
from odyssey_exchange_api.requests.base import BaseRequest


class SpotKlineDataRequest(BaseRequest[list[SpotKlineData]]):
    """
    Retrieve Kline/candlestick data. Returns an array of :class:`SpotKlineData`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/spot-trading-api#kline-candlestick-data
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/klines"

    __returning__ = list[SpotKlineData]

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    interval: str
    """Interval of the Kline. Possible values include: 1min, 5min, 15min, 30min, 60min, 1day, 1week, 1month."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 300."""
