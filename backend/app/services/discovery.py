from datetime import datetime

from app.schemas.discovery import DiscoveredToken, DiscoveryStatus


def get_recent_discoveries() -> list[DiscoveredToken]:
    return [
        DiscoveredToken(
            name="Example Meme Token",
            symbol="MEME",
            token_address="7YxExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:30:00-04:00"
            ),
            status=DiscoveryStatus.NEW,
        ),
        DiscoveredToken(
            name="Moon Dog",
            symbol="MDOG",
            token_address="9AbExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:32:00-04:00"
            ),
            status=DiscoveryStatus.WATCHING,
        ),
        DiscoveredToken(
            name="Solana Frog",
            symbol="FROG",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
        DiscoveredToken(
            name="Sol Bull",
            symbol="sb",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
                DiscoveredToken(
            name="Example Meme Token",
            symbol="MEME",
            token_address="7YxExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:30:00-04:00"
            ),
            status=DiscoveryStatus.NEW,
        ),
        DiscoveredToken(
            name="Moon Dog",
            symbol="MDOG",
            token_address="9AbExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:32:00-04:00"
            ),
            status=DiscoveryStatus.WATCHING,
        ),
        DiscoveredToken(
            name="Solana Frog",
            symbol="FROG",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
        DiscoveredToken(
            name="Sol Bull",
            symbol="sb",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
                DiscoveredToken(
            name="Example Meme Token",
            symbol="MEME",
            token_address="7YxExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:30:00-04:00"
            ),
            status=DiscoveryStatus.NEW,
        ),
        DiscoveredToken(
            name="Moon Dog",
            symbol="MDOG",
            token_address="9AbExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:32:00-04:00"
            ),
            status=DiscoveryStatus.WATCHING,
        ),
        DiscoveredToken(
            name="Solana Frog",
            symbol="FROG",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
        DiscoveredToken(
            name="Sol Bull",
            symbol="sb",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
                DiscoveredToken(
            name="Example Meme Token",
            symbol="MEME",
            token_address="7YxExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:30:00-04:00"
            ),
            status=DiscoveryStatus.NEW,
        ),
        DiscoveredToken(
            name="Moon Dog",
            symbol="MDOG",
            token_address="9AbExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:32:00-04:00"
            ),
            status=DiscoveryStatus.WATCHING,
        ),
        DiscoveredToken(
            name="Solana Frog",
            symbol="FROG",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
        DiscoveredToken(
            name="Sol Bull",
            symbol="sb",
            token_address="3CdExampleTokenAddress123456789ABCDEFG",
            source="DexScreener",
            discovered_at=datetime.fromisoformat(
                "2026-08-12T18:35:00-04:00"
            ),
            status=DiscoveryStatus.GRADUATED,
        ),
    ]