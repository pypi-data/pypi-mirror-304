from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import BaseRequest, SignedRequest
from odyssey_exchange_api.responses import FuturesOrderIDResponse


class FuturesCancelOrderRequest(SignedRequest[FuturesOrderIDResponse]):
    """
    Cancel an order. Returns an array of :class:`odyssey_exchange_api.responses.FuturesOrderIDResponse`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#cancel-order
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/cancel"

    __returning__ = FuturesOrderIDResponse

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    order_id: str = Field(serialization_alias="orderId")
    """Order ID."""
