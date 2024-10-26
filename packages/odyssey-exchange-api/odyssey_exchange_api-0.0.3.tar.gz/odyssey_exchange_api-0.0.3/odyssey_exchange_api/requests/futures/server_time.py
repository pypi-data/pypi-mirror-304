from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesServerTime
from odyssey_exchange_api.requests.base import BaseRequest


class FuturesServerTimeRequest(BaseRequest[FuturesServerTime]):
    """
    This interface checks connectivity to the server and retrieves server timestamp. Returns a :class:`odyssey_exchange_api.objects.FuturesServerTime`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#check-server-time
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/time"

    __returning__ = FuturesServerTime
