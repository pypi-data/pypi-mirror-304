from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesTickerData
from odyssey_exchange_api.requests.base import BaseRequest


class FuturesTickerDataRequest(BaseRequest[FuturesTickerData]):
    """
    Retrieve 24-hour price change data, returns a :class:`odyssey_exchange_api.objects.FuturesTickerData`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#id-24hrs-ticker
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/ticker"

    __returning__ = FuturesTickerData

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
