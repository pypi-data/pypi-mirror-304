import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesPositionType, FuturesOrderSide, FuturesPositionStatus, \
    FuturesPositionFrozenStatus


class FuturesAccountPosition(BaseModel):
    """
    An object that contains information about the user position.
    """

    id: int
    """Position id"""
    uid: int
    """User ID"""
    contract_id: int = Field(alias="contractId")
    """Contract ID"""
    position_type: FuturesPositionType = Field(alias="positionType")
    """Position type"""
    side: FuturesOrderSide
    """Position side"""
    volume: Decimal
    """Position quantity"""
    open_price: Decimal = Field(alias="openPrice")
    """Opening price"""
    average_price: Decimal = Field(alias="avgPrice")
    """Average position price"""
    close_price: Decimal = Field(alias="closePrice")
    """Average closing price"""
    leverage_level: int = Field(alias="leverageLevel")
    """Leverage multiple"""
    open_amount: Decimal = Field(alias="openAmount")
    """Opening margin"""
    hold_amount: Decimal = Field(alias="holdAmount")
    """Position margin"""
    close_volume: Decimal = Field(alias="closeVolume")
    """Quantity of positions closed"""
    pending_close_volume: Decimal = Field(alias="pendingCloseVolume")
    """The volume of place closing orders"""
    realized_amount: Decimal = Field(alias="realizedAmount")
    """Realized profit and loss"""
    history_realized_amount: Decimal = Field(alias="historyRealizedAmount")
    """Historical accumulated profit and loss"""
    trade_fee: Decimal = Field(alias="tradeFee")
    """Transaction Fees"""
    capital_fee: Decimal = Field(alias="capitalFee")
    """Funding charges"""
    close_profit: Decimal = Field(alias="closeProfit")
    """Position closing profit and loss"""
    share_amount: Decimal = Field(alias="shareAmount")
    """Sharing amount"""
    freeze_lock: FuturesPositionFrozenStatus = Field(alias="freezeLock")
    """Position frozen status"""
    status: FuturesPositionStatus
    """Position validity"""
    ctime: datetime.datetime
    """Creation time"""
    mtime: datetime.datetime
    """Update time"""
    brokerId: int
    """Broker id"""
    lock_time: datetime.datetime = Field(alias="lockTime")
    """Liquidation lock time"""
    margin_rate: Decimal = Field(alias="marginRate")
    """Margin rate"""
    reduce_price: Decimal = Field(alias="reducePrice")
    """Forced price reduction"""
    return_rate: Decimal = Field(alias="returnRate")
    """Rate of return (yield)"""
    unrealized_amount: Decimal = Field(alias="unRealizedAmount")
    """Unrealized profit or loss"""
    open_realized_amount: Decimal = Field(alias="openRealizedAmount")
    """Unrealized profit and loss on opening a position"""
    position_balance: Decimal = Field(alias="positionBalance")
    """Position value"""
    settle_profit: Decimal = Field(alias="settleProfit")
    """Position settlement"""
    index_price: Decimal = Field(alias="indexPrice")
    """Latest index price"""
    keep_rate: Decimal = Field(alias="keepRate")
    """Tiered Minimum Maintenance Margin Rate"""
    max_fee_rate: Decimal = Field(alias="maxFeeRate")
    """Maximum handling fee for closing the position"""
