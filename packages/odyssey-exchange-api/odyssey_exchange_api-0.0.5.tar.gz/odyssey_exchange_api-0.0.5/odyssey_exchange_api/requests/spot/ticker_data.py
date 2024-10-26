from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotTickerData
from odyssey_exchange_api.requests.base import BaseRequest


class SpotTickerDataRequest(BaseRequest[SpotTickerData]):
    """
    Retrieve 24-hour price change data, returns a :class:`odyssey_exchange_api.objects.SpotTickerData`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/spot-trading-api#id-24hrs-ticker
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/ticker"

    __returning__ = SpotTickerData

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
