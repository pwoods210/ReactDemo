from sqlalchemy.orm import Session

from app.database.models import Discovery
from app.database.repository import get_active_discoveries


def get_recent_discoveries(
    session: Session,
) -> list[Discovery]:
    return get_active_discoveries(
        session,
        limit=50,
    )