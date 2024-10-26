from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotMyTrade
from odyssey_exchange_api.requests.base import SignedRequest


class SpotMyTradesRequest(SignedRequest[list[SpotMyTrade]]):
    """
    Get a list of your own trades. Returns an array of :class:`SpotMyTrade`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/myTrades"

    __returning__ = list[SpotMyTrade]

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 1000."""
