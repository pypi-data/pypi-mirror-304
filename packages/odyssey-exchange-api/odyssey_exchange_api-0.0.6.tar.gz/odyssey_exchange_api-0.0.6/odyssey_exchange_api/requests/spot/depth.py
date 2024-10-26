from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.requests.base import BaseRequest
from odyssey_exchange_api.responses import SpotDepthResponse


class SpotDepthRequest(BaseRequest[SpotDepthResponse]):
    """
    Market depth data. Returns a :class:`odyssey_exchange_api.responses.SpotDepthResponse`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/depth"

    __returning__ = SpotDepthResponse

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 100."""
