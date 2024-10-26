from pydantic import Field

from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.requests.base import SignedRequest
from odyssey_exchange_api.responses import SpotBatchCancelOrderResponse


class SpotBatchCancelOrderRequest(SignedRequest[SpotBatchCancelOrderResponse]):
    """
    Mass cancellation of orders, maximum 10 orders at a time. Returns a :class:`odyssey_exchange_api.responses.SpotBatchCancelOrderResponse`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "POST"
    _request_path = "/sapi/v1/batchCancel"

    __returning__ = SpotBatchCancelOrderResponse

    order_ids: list[int] = Field(serialization_alias="orderIds")
    """Array of order ids."""
    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
