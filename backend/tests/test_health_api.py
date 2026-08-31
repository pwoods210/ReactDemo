from fastapi.testclient import TestClient

from app.main import app
import app.api.health as health_api


def test_api_health_endpoint_returns_true():
    response = TestClient(app).get("/health/api")

    assert response.status_code == 200
    assert response.json() is True


def test_services_health_reports_dependency_states(monkeypatch):
    monkeypatch.setattr(health_api, "discovery_is_alive", lambda: True)
    monkeypatch.setattr(health_api, "database_is_alive", lambda: False)

    response = TestClient(app).get("/health/services")

    assert response.status_code == 200
    assert response.json() == {
        "discovery": {"status": "up"},
        "trade": {"status": "down"},
        "database": {"status": "down"},
    }


def test_discovery_heartbeat_endpoint_records_heartbeat(monkeypatch):
    calls = []
    monkeypatch.setattr(
        health_api,
        "record_discovery_heartbeat",
        lambda: calls.append("heartbeat"),
    )

    response = TestClient(app).post("/health/discovery/heartbeat")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert calls == ["heartbeat"]
