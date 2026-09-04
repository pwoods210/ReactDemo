from datetime import datetime
from enum import StrEnum
from typing import Any

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
    pair_address: str | None = Field(default=None, alias="pairAddress")
    source: str
    exchange: str | None = None
    discovered_at: datetime = Field(alias="discoveredAt")
    status: DiscoveryStatus
    graduated_at: datetime | None = Field(default=None, alias="graduatedAt")
    token_profile: dict[str, Any] = Field(
        default_factory=dict,
        alias="tokenProfile",
    )
    pairs_data: list[dict[str, Any]] = Field(
        default_factory=list,
        alias="pairs",
    )
