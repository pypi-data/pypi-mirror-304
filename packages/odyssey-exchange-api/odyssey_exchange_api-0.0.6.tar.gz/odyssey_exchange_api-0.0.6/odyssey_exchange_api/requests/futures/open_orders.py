from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesOrder
from odyssey_exchange_api.requests.base import SignedRequest


class FuturesOpenOrdersRequest(SignedRequest[list[FuturesOrder]]):
    """
    Get a list of open orders. Returns an array of :class:`odyssey_exchange_api.objects.FuturesOrder`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/openOrders"

    __returning__ = list[FuturesOrder]

    contract_name: str = Field(serialization_alias="contractName")
    """The lowercase symbol name, e.g., btcusdt."""
