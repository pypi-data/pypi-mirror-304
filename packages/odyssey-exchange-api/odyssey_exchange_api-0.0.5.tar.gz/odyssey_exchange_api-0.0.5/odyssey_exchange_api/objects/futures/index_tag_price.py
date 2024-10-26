from decimal import Decimal

from pydantic import BaseModel, Field


class FuturesIndexTagPrice(BaseModel):
    """
    An object that contains information about the index price, tag price and funding data.
    """

    index_price: Decimal = Field(alias="indexPrice")
    """Index price"""
    tag_price: Decimal = Field(alias="tagPrice")
    """Tag price"""
    next_fund_rate: Decimal = Field(alias="nextFundRate")
    """Funding rate price"""
    current_fund_rate: Decimal = Field(alias="currentFundRate")
    """Funding rate price for the previous period (used for settlement in this period)"""
