from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotOrder
from odyssey_exchange_api.requests.base import SignedRequest


class SpotOpenOrdersRequest(SignedRequest[list[SpotOrder]]):
    """
    Get a list of open orders. Returns an array of :class:`odyssey_exchange_api.objects.SpotOrder`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/spot-trading-api#current-open-orders
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/openOrders"

    __returning__ = list[SpotOrder]

    symbol: str
    """The lowercase symbol name, e.g., btcusdt."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 1000."""
