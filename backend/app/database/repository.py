from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Discovery


def get_active_discoveries(
    session: Session,
    limit: int = 50,
) -> list[Discovery]:
    statement = (
        select(Discovery)
        .where(Discovery.dismissed_at.is_(None))
        .order_by(Discovery.discovered_at.desc())
        .limit(limit)
    )

    return list(
        session.scalars(statement)
    )