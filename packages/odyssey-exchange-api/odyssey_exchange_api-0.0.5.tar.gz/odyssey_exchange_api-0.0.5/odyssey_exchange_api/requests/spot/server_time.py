from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.objects import SpotServerTime
from odyssey_exchange_api.requests.base import BaseRequest


class SpotServerTimeRequest(BaseRequest[SpotServerTime]):
    """
    This interface checks connectivity to the server and retrieves server timestamp. Returns a :class:`odyssey_exchange_api.objects.ServerTime`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/spot-trading-api#check-server-time
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/time"

    __returning__ = SpotServerTime
