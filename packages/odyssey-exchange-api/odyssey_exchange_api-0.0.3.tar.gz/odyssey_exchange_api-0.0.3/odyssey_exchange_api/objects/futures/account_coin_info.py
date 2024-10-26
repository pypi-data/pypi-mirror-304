from decimal import Decimal

from pydantic import BaseModel, Field

from .account_positions import FuturesAccountPositions


class FuturesAccountCoinInfo(BaseModel):
    """
    An object that contains information about the coin at user's account.
    """

    margin_coin: str = Field(alias="marginCoin")
    """Margin currency"""
    account_normal: Decimal = Field(alias="accountNormal")
    """Account balance"""
    account_lock: Decimal = Field(alias="accountLock")
    """Margin frozen account"""
    part_position_normal: Decimal = Field(alias="partPositionNormal")
    """Isolated margin balance"""
    total_position_normal: Decimal = Field(alias="totalPositionNormal")
    """Initial margin occupied by full position"""
    achieved_amount: Decimal = Field(alias="achievedAmount")
    """Realized profit and loss"""
    unrealized_amount: Decimal = Field(alias="unrealizedAmount")
    """Unrealized profit or loss"""
    total_margin_rate: Decimal = Field(alias="totalMarginRate")
    """Cross Margin Rate"""
    total_equity: Decimal = Field(alias="totalEquity")
    """Cross Margin Interest"""
    part_equity: Decimal = Field(alias="partEquity")
    """Isolated interest"""
    total_cost: Decimal = Field(alias="totalCost")
    """Cost of occupying the entire warehouse"""
    sum_margin_rate: Decimal = Field(alias="sumMarginRate")
    """Margin rate for all accounts"""
    position_vos: list[FuturesAccountPositions] = Field(alias="positionVos")
    """Position contract records"""
