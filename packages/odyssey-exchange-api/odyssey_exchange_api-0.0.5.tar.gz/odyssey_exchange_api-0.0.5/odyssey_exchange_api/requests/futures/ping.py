from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import BaseRequest


class FuturesPingRequest(BaseRequest[dict]):
    """
    This interface checks connectivity to the host. Returns an empty :class:`dict`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#test-connectivity
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/ping"

    __returning__ = dict
