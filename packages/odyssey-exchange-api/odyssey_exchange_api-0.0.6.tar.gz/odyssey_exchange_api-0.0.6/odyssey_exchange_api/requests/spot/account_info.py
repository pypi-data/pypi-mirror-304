from odyssey_exchange_api.base import BASE_SPOT_URL
from odyssey_exchange_api.requests.base import SignedRequest
from odyssey_exchange_api.responses import SpotAccountInfoResponse


class SpotAccountInfoRequest(SignedRequest[SpotAccountInfoResponse]):
    """
    Get account information. Returns a :class:`odyssey_exchange_api.responses.SpotAccountInfoResponse`.
    """

    _request_url = BASE_SPOT_URL
    _request_method = "GET"
    _request_path = "/sapi/v1/account"

    __returning__ = SpotAccountInfoResponse
