from pydantic import BaseModel, Field


class FuturesServerTime(BaseModel):
    """
    An object that contains information about the time zone and the current timestamp.
    """

    timezone: str
    """Server timezone"""
    server_time: int = Field(alias="serverTime")
    """Current timestamp"""
