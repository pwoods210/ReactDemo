from datetime import datetime

from app.schemas.discovery import DiscoveredToken, DiscoveryStatus


def get_recent_discoveries() -> list[DiscoveredToken]:
    return [
        DiscoveredToken(
            name="Example Meme Token 2",
            symbol="MEME",
            token_address="7YxExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-05T21:00:00-04:00"
            ),
            status=DiscoveryStatus.NEW,
        )
    ]