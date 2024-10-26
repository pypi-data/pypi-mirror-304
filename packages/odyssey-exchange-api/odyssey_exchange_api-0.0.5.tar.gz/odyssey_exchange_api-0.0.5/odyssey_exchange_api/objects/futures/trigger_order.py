from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesOrderSide, FuturesPositionSide, FuturesTriggerType, \
    FuturesTriggerOrderStatus


class FuturesTriggerOrder(BaseModel):
    """
    An object that contains information about the trigger order.
    """

    id: int
    """Trigger order collection table id"""
    trigger_order_id: int = Field(alias="triggerOrderId")
    """Trigger order ID"""
    contract_id: int = Field(alias="contractId")
    """Contract ID"""
    contract_name: str = Field(alias="contractName")
    """Contract name"""
    margin_coin: str = Field(alias="marginCoin")
    """Margin currenct"""
    multiplier: Decimal
    """Contract value"""
    trigger_price: Decimal = Field(alias="triggerPrice")
    """Trigger price"""
    price: Decimal
    """Price"""
    price_precision: int = Field(alias="pricePrecision")
    """Price accuracy"""
    volume: Decimal
    """Order volume"""
    open: FuturesPositionSide
    """Direction of opening and closing positions"""
    side: FuturesOrderSide
    """Order side"""
    status: FuturesTriggerOrderStatus
    """Valid status"""
    expire_time: int = Field(alias="expireTime")
    """Order expiration time"""
    ctime: int
    """Creation time"""
    mtime: int
    """Modify time"""
    trigger_type: FuturesTriggerType = Field(alias="triggerType")
    """Trigger order type"""
