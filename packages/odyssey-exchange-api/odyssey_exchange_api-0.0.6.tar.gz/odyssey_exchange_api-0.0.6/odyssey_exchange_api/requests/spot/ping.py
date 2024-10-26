from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.requests.base import BaseRequest


class SpotPingRequest(BaseRequest[dict]):
    """
    This interface checks connectivity to the host. Returns an empty :class:`dict`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/ping"

    __returning__ = dict
