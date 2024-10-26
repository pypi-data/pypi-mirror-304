from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesIndexTagPrice
from odyssey_exchange_api.requests.base import BaseRequest


class FuturesIndexTagPriceRequest(BaseRequest[FuturesIndexTagPrice]):
    """
    Getting index and tag prices and additional funding data. Returns a :class:`odyssey_exchange_api.objects.FuturesIndexTagPrice`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/index"

    __returning__ = FuturesIndexTagPrice

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
