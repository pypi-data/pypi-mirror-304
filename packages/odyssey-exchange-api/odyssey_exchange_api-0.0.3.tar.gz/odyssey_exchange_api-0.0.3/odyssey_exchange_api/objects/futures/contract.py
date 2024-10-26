from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesContractSide, FuturesContractStatus, FuturesContractType


class FuturesContract(BaseModel):
    """
    An object that contains information about the futures contract.
    """

    symbol: str
    """The uppercase contract name, e.g., E-BTC-USDT."""
    contract_id: int = Field(alias="contractId")
    """Contract ID"""
    price_precision: int = Field(alias="pricePrecision")
    """Price accuracy"""
    status: FuturesContractStatus
    """Contract status"""
    type: FuturesContractType
    """Contract type"""
    side: FuturesContractSide
    """Contract direction"""
    multiplier: Decimal
    """Contract value"""
    multiplierCoin: str
    """Contract coin"""
    min_order_volume: Decimal = Field(alias="minOrderVolume")
    """Minimum order quantity"""
    min_order_money: Decimal = Field(alias="minOrderMoney")
    """Minimum order amount"""
    max_market_volume: Decimal = Field(alias="maxMarketVolume")
    """Maximum order quantity for market orders"""
    max_market_money: Decimal = Field(alias="maxMarketMoney")
    """Maximum order amount at market price"""
    max_limit_volume: Decimal = Field(alias="maxLimitVolume")
    """Maximum order quantity for limit orders"""
    max_limit_money: Decimal = Field(alias="maxLimitMoney")
    """Limit price maximum order amount"""
    max_valid_orders: Decimal = Field(alias="maxValidOrder")
    """The maximum number of valid orders"""
