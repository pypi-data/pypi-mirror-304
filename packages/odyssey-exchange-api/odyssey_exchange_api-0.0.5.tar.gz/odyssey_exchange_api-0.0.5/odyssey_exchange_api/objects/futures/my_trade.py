from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesOrderSide


class FuturesMyTrade(BaseModel):
    """
    An object that contains information about my trades.
    """

    contract_name: str = Field(validation_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    trade_id: int = Field(validation_alias="tradeId")
    """Trade ID"""
    bid_id: int = Field(alias="bidId")
    """Buy side order ID"""
    ask_id: int = Field(alias="askId")
    """Sell side order ID"""
    price: Decimal
    """Trade price"""
    quantity: Decimal = Field(alias="qty")
    """Trade volume"""
    amount: Decimal
    """Trade amount"""
    time: int
    """Trade timestamp"""
    is_buyer: bool = Field(alias="isBuyer")
    """if True it is buyer, else seller"""
    is_maker: bool = Field(alias="isMaker")
    """If True it is Maker, else taker"""
    fee: Decimal
    """Trade fee"""
    bid_user_id: int = Field(alias="bidUserId")
    """Buy side user id"""
    ask_user_id: int = Field(alias="askUserId")
    """Sell side user id"""
    side: FuturesOrderSide
    """Order side"""
