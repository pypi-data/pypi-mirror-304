from pydantic import BaseModel, Field


class SpotAssetPair(BaseModel):
    """
    An object that contains information about the asset.
    """

    symbol: str
    """The lowercase symbol name, e.g., btcusdt."""
    base_asset: str = Field(alias="baseAsset")
    """Underlying asset for the symbol"""
    quote_asset: str = Field(alias="quoteAsset")
    """Quote asset for the symbol"""
    price_precision: int = Field(alias="pricePrecision")
    """Price accuracy"""
    quantity_precision: int = Field(alias="quantityPrecision")
    """Quantity accuracy"""
