from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import BaseRequest
from odyssey_exchange_api.responses import FuturesDepthResponse


class FuturesDepthRequest(BaseRequest[FuturesDepthResponse]):
    """
    Market depth data. Returns a :class:`odyssey_exchange_api.responses.FuturesDepthResponse`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#depth
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/depth"

    __returning__ = FuturesDepthResponse

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    limit: int = 100
    """The maximum number of items that can be returned in the query result. The value must be a positive integer. The default value is 100, maximum value is 100."""
