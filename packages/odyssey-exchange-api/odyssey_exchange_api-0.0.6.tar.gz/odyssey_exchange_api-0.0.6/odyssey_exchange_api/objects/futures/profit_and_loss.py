from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesOrderSide, FuturesPositionType


class FuturesProfitAndLoss(BaseModel):
    """
    An object that contains information about profit and losses.
    """

    side: FuturesOrderSide
    """Order side"""
    position_type: FuturesPositionType = Field(validation_alias="positionType")
    """Position type"""
    trade_fee: Decimal = Field(validation_alias="tradeFee")
    """Trade fee"""
    realized_amount: Decimal = Field(validation_alias="realizedAmount")
    """Realized amount"""
    leverage_level: int = Field(validation_alias="leverageLevel")
    """Leverage level"""
    open_price: Decimal = Field(validation_alias="openPrice")
    """Open price"""
    settle_profit: Decimal | None = Field(validation_alias="settleProfit", default=None)
    mtime: int
    """Modify time"""
    share_amount: Decimal = Field(validation_alias="shareAmount")
    """Share amount"""
    open_end_price: Decimal = Field(validation_alias="openEndPrice")
    """Open end price"""
    close_profit: Decimal = Field(validation_alias="closeProfit")
    """Close profit"""
    volume: Decimal
    """Volume"""
    contract_id: int = Field(validation_alias="contractId")
    """Contract ID"""
    history_realized_amount: Decimal = Field(validation_alias="historyRealizedAmount")
    """History realized amount"""
    ctime: int
    """Creation time"""
    id: int
    """ID"""
    capital_fee: Decimal = Field(validation_alias="capitalFee")
    """Capital fee"""
