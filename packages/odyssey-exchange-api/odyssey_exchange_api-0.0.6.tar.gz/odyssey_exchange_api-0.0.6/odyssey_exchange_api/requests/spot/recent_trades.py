from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotRecentTrade
from odyssey_exchange_api.requests.base import BaseRequest


class SpotRecentTradesRequest(BaseRequest[list[SpotRecentTrade]]):
    """
    Fetch recent trades for the specified asset. Returns an array of :class:`odyssey_exchange_api.objects.SpotRecentTrade`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/trades"

    __returning__ = list[SpotRecentTrade]

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 1000."""
