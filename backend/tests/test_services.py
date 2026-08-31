import app.services.discovery as discovery_service


def test_get_recent_discoveries_requests_fifty_active_records(monkeypatch):
    calls = {}

    def fake_get_active_discoveries(session, limit):
        calls["session"] = session
        calls["limit"] = limit
        return ["discovery"]

    monkeypatch.setattr(
        discovery_service,
        "get_active_discoveries",
        fake_get_active_discoveries,
    )

    session = object()
    result = discovery_service.get_recent_discoveries(session)

    assert result == ["discovery"]
    assert calls == {"session": session, "limit": 50}
