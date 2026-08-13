from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.discovery import DiscoveredToken
from app.services.discovery import get_recent_discoveries


router = APIRouter(
    prefix="/api/discoveries",
    tags=["discoveries"],
)


@router.get(
    "",
    response_model=list[DiscoveredToken],
    response_model_by_alias=True,
)
def get_discoveries(
    session: Session = Depends(get_db),
) -> list[DiscoveredToken]:
    return get_recent_discoveries(session)