from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Discovery(Base):
    __tablename__ = "discoveries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    token_address: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    pair_address: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    symbol: Mapped[str] = mapped_column(
        String(32),
    )

    source: Mapped[str] = mapped_column(
        String(64),
    )

    exchange: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        default="new",
    )

    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    graduated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    dismissed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )