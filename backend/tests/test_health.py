from datetime import datetime, timedelta, timezone

import app.services.health as health


def test_discovery_is_not_alive_before_first_heartbeat(monkeypatch):
    monkeypatch.setattr(health, "_last_discovery_heartbeat", None)

    assert health.discovery_is_alive() is False


def test_recent_discovery_heartbeat_is_alive(monkeypatch):
    monkeypatch.setattr(health, "_last_discovery_heartbeat", None)

    health.record_discovery_heartbeat()

    assert health.discovery_is_alive() is True


def test_expired_discovery_heartbeat_is_not_alive(monkeypatch):
    expired_at = datetime.now(timezone.utc) - timedelta(seconds=16)
    monkeypatch.setattr(health, "_last_discovery_heartbeat", expired_at)

    assert health.discovery_is_alive(timeout_seconds=15) is False
