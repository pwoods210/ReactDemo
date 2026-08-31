from datetime import datetime, timezone

from app.schemas.discovery import DiscoveredToken


def test_discovered_token_accepts_database_names_and_serializes_api_aliases():
    discovered_at = datetime.now(timezone.utc)
    token = DiscoveredToken.model_validate(
        {
            "id": 1,
            "name": "Example Token",
            "symbol": "EXAMPLE",
            "token_address": "token-123",
            "source": "DexScreener",
            "discovered_at": discovered_at,
            "status": "watching",
        }
    )

    payload = token.model_dump(by_alias=True)

    assert token.token_address == "token-123"
    assert payload["tokenAddress"] == "token-123"
    assert payload["discoveredAt"] == discovered_at
