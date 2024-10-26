from pydantic import BaseModel

from odyssey_exchange_api.objects import SpotAssetBalance


class SpotAccountInfoResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.SpotAccountInfoRequest`.

    Contains an account balances.
    """

    balances: list[SpotAssetBalance]
    """Array of :class:`odyssey_exchange_api.objects.SpotAssetBalance`."""
