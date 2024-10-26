from pydantic import Field

from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.requests.base import SignedRequest
from odyssey_exchange_api.responses import SpotCancelOrderResponse


class SpotCancelOrderRequest(SignedRequest[SpotCancelOrderResponse]):
    """
    Cancel an order. Returns a :class:`odyssey_exchange_api.responses.SpotCancelOrderResponse`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/spot-trading-api#cancel-order
    """

    _request_url = BASE_SPOT_URL
    _request_method = "POST"
    _request_path = "/sapi/v1/cancel"

    __returning__ = SpotCancelOrderResponse

    order_id: str = Field(serialization_alias="orderId")
    """Order ID."""
    symbol: str
    """The lowercase symbol name, e.g., btcusdt."""
