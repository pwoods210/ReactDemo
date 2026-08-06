from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import DiscoveredToken, DiscoveryStatus


app = FastAPI(
    title="Meme Trade API",
    description="Backend API for token discovery and trade operations.",
    version="0.1.0",
)

# The React development server runs on a different browser origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/api/discoveries",
    response_model=list[DiscoveredToken],
    response_model_by_alias=True,
)
def get_discoveries() -> list[DiscoveredToken]:
    return [
        DiscoveredToken(
            name="Fresh Meme of the Day",
            symbol="MEME",
            token_address="7YxExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-05T21:00:00-04:00"
            ),
            status=DiscoveryStatus.NEW,
        )
    ]