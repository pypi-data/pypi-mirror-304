from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.objects import FuturesContract
from odyssey_exchange_api.requests.base import BaseRequest


class FuturesContractsListRequest(BaseRequest[list[FuturesContract]]):
    """
    Get a list of all contracts on the exchange. Returns an array of :class:`odyssey_exchange_api.objects.FuturesContract`.

    Source: https://exchangeopenapi.gitbook.io/pri-openapi/openapi-doc/futures-trading-api#contracts-list
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "GET"
    _request_path = "/fapi/v1/contracts"

    __returning__ = list[FuturesContract]
