from pydantic import BaseModel

from odyssey_exchange_api.objects import SpotAssetPair


class SpotPairListResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.SpotPairListRequest`.

    Contains a data of asset pairs at exchange.
    """

    symbols: list[SpotAssetPair]
    """Array of :class:`odyssey_exchange_api.objects.SpotAssetPair`"""
