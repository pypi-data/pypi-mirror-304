from pydantic import BaseModel

from odyssey_exchange_api.objects import FuturesAccountCoinInfo


class FuturesAccountInfoResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.FuturesAccountInfoRequest`.

    An object with information about requested account.
    """

    account: list[FuturesAccountCoinInfo]
    """Array with information about coins at account"""
