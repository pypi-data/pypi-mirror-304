from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import SignedRequest, ResponseType
from odyssey_exchange_api.responses import FuturesCurrentTriggerOrdersResponse


class FuturesCurrentTriggerOrdersRequest(SignedRequest[FuturesCurrentTriggerOrdersResponse]):
    """
    Get all trigger orders. Returns a :class:`odyssey_exchange_api.responses.FuturesCurrentTriggerOrdersResponse`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/trigger_order_list"

    __returning__ = FuturesCurrentTriggerOrdersResponse

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    page: int
    """Current page number"""
    limit: int
    """Total data per page, maximum is 1000"""

    def make_response(self, data) -> ResponseType:
        return super().make_response(data["data"])
