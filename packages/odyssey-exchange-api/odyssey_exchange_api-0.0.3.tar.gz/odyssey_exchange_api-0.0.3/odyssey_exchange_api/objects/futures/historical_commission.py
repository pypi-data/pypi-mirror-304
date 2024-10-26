import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesOrderSide, FuturesPositionType, FuturesPositionSide


class FuturesHistoricalCommission(BaseModel):
    """
    An object that contains information about the historical commission at positions.
    """

    side: FuturesOrderSide
    """Order side"""
    client_id: str = Field(validation_alias="clientId")
    ctime_ms: int = Field(validation_alias="ctimeMs")
    """Creation time at milliseconds"""
    position_type: FuturesPositionType = Field(validation_alias="positionType")
    """Position type"""
    order_id: int = Field(validation_alias="orderId")
    """Order ID"""
    average_price: Decimal | None = Field(validation_alias="avgPrice", default=None)
    """Average order price"""
    open_or_close: FuturesPositionSide = Field(validation_alias="openOrClose")
    """Position side"""
    leverage_level: int = Field(validation_alias="leverageLevel")
    """Leverage level"""
    type: int
    close_taker_fee_rate: Decimal = Field(validation_alias="closeTakerFeeRate")
    """Close taker fee rate"""
    open_maker_fee_rate: Decimal = Field(validation_alias="openMakerFeeRate")
    """Open maker fee rate"""
    close_maker_fee_rate: Decimal = Field(validation_alias="closeMakerFeeRate")
    """Close maker fee rate"""
    open_taker_fee_rate: Decimal = Field(validation_alias="openTakerFeeRate")
    """Open taker fee rate"""
    volume: Decimal
    """Volume"""
    deal_volume: Decimal = Field(validation_alias="dealVolume")
    """Deal volume"""
    price: Decimal | None = None
    """Price"""
    contract_id: int = Field(validation_alias="contractId")
    """Contract ID"""
    ctime: datetime.datetime
    """Creation date"""
    contractName: str = Field(validation_alias="contractName")
    """Contract name"""
    deal_money: Decimal = Field(validation_alias="dealMoney")
    """Deal money"""
    status: int
    """Status"""
