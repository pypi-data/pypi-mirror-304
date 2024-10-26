from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotSingleBatchOrder
from odyssey_exchange_api.requests.base import SignedRequest
from odyssey_exchange_api.responses import SpotBatchOrdersResponse


class SpotBatchOrdersRequest(SignedRequest[SpotBatchOrdersResponse]):
    """
    Place batch orders. Returns a :class:`odyssey_exchange_api.responses.SpotBatchOrdersResponse`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "POST"
    _request_path = "/sapi/v1/batchOrders"

    __returning__ = SpotBatchOrdersResponse

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    orders: list[SpotSingleBatchOrder]
    """An array of orders, with a maximum of 10 orders in the array."""
