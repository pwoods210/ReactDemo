from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DiscoveryStatus(StrEnum):
    NEW = "new"
    WATCHING = "watching"
    GRADUATED = "graduated"


class DiscoveredToken(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    id: int
    name: str
    symbol: str
    token_address: str = Field(alias="tokenAddress")
    source: str
    discovered_at: datetime = Field(alias="discoveredAt")
    status: DiscoveryStatus