from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesHistoricalCommission
from odyssey_exchange_api.requests.base import SignedRequest


class FuturesHistoricalCommissionRequest(SignedRequest[list[FuturesHistoricalCommission]]):
    """
    Receives data on the historical commission. Returns an array of :class:`odyssey_exchange_api.objects.FuturesHistoricalCommission`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/orderHistorical"

    __returning__ = list[FuturesHistoricalCommission]

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 1000."""
    from_id: int | None = Field(serialization_alias="fromId", default=None)
    """Start searching from this record"""
