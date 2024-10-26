from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import SpotOrderSide


class SpotMyTrade(BaseModel):
    """
    An object that contains information about my trades.
    """

    symbol: str
    """The uppercase symbol name, e.g., BTCUSDT."""
    id: int
    """Trade ID"""
    bid_id: int = Field(alias="bidId")
    """Buy side order ID"""
    ask_id: int = Field(alias="askId")
    """Sell side order ID"""
    price: Decimal
    """Trade price"""
    quantity: Decimal = Field(alias="qty")
    """Trade volume"""
    time: int
    """Trade timestamp"""
    is_buyer: bool = Field(alias="isBuyer")
    """if True it is buyer, else seller"""
    is_maker: bool = Field(alias="isMaker")
    """If True it is Maker, else taker"""
    fee_coin: str = Field(alias="feeCoin")
    """Trade fee coin"""
    fee: Decimal
    """Trade fee"""
    bid_user_id: int = Field(alias="bidUserId")
    """Buy side user id"""
    ask_user_id: int = Field(alias="askUserId")
    """Sell side user id"""
    is_self: bool = Field(alias="isSelf")
    """Self deal status, true if self deal, else not self deal"""
    side: SpotOrderSide
    """Order side"""
