from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.requests.base import BaseRequest
from odyssey_exchange_api.responses import SpotPairListResponse


class SpotPairListRequest(BaseRequest[SpotPairListResponse]):
    """
    The supported symbol pair collection which in the exchange. Returns a :class:`odyssey_exchange_api.responses.SpotPairListResponse`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/symbols"

    __returning__ = SpotPairListResponse
