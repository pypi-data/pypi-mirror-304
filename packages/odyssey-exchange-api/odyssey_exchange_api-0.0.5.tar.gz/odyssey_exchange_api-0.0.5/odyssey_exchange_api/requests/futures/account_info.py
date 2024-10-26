from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.requests.base import SignedRequest


from odyssey_exchange_api.responses import FuturesAccountInfoResponse


class FuturesAccountInfoRequest(SignedRequest[FuturesAccountInfoResponse]):
    """
    Get account information. Returns a :class:`odyssey_exchange_api.responses.FuturesAccountInfoResponse`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#account-information
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/account"

    __returning__ = FuturesAccountInfoResponse
