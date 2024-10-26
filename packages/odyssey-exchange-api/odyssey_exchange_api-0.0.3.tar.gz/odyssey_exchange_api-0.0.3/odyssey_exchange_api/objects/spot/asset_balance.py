from decimal import Decimal

from pydantic import BaseModel


class SpotAssetBalance(BaseModel):
    """
    An object that contains information about the amount of assets, available assets, and locked assets.
    """

    asset: str
    """Coin name"""
    free: Decimal
    """Account available amount"""
    locked: Decimal
    """Account frozen amount"""
