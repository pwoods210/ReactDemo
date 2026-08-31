from datetime import datetime, timezone
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.discoveries import get_db
from app.main import app
import app.api.discoveries as discoveries_api


def test_get_discoveries_returns_camel_case_api_contract(monkeypatch):
    discovery = SimpleNamespace(
        id=1,
        name="Example Token",
        symbol="EXAMPLE",
        token_address="token-123",
        source="DexScreener",
        discovered_at=datetime(2026, 8, 31, tzinfo=timezone.utc),
        status="new",
    )

    monkeypatch.setattr(
        discoveries_api,
        "get_recent_discoveries",
        lambda session: [discovery],
    )
    app.dependency_overrides[get_db] = lambda: object()

    try:
        response = TestClient(app).get("/api/discoveries")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Example Token",
            "symbol": "EXAMPLE",
            "tokenAddress": "token-123",
            "source": "DexScreener",
            "discoveredAt": "2026-08-31T00:00:00Z",
            "status": "new",
        }
    ]
