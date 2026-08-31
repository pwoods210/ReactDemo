import asyncio
from datetime import timedelta
from types import SimpleNamespace

import pytest

import app.workers.listener as listener


@pytest.mark.parametrize(
    ("dex_id", "expected"),
    [
        ("pumpfun", "pumpfun"),
        ("PumpSwap", "pumpswap"),
        ("RAYDIUM", "raydium"),
    ],
)
def test_classify_pair_normalizes_supported_exchanges(dex_id, expected):
    assert listener.classify_pair({"dexId": dex_id}) == expected


def test_classify_pair_rejects_unsupported_exchanges():
    assert listener.classify_pair({"dexId": "orca"}) is None
    assert listener.classify_pair({}) is None


def test_add_to_graduation_watch_is_idempotent(monkeypatch):
    watch = {}
    monkeypatch.setattr(listener, "graduation_watch", watch)

    profile = {"tokenAddress": "token-123"}
    listener.add_to_graduation_watch("token-123", profile)
    listener.add_to_graduation_watch("token-123", {"different": True})

    assert list(watch) == ["token-123"]
    assert watch["token-123"]["token_profile"] == profile


def test_handle_token_profile_ignores_non_solana_tokens(monkeypatch):
    async def fail_if_hydrated(*args, **kwargs):
        raise AssertionError("non-Solana token was hydrated")

    monkeypatch.setattr(listener, "hydrate_token", fail_if_hydrated)

    asyncio.run(
        listener.handle_token_profile(
            object(),
            {"chainId": "ethereum", "tokenAddress": "token-123"},
        )
    )


def test_handle_token_profile_watches_pumpfun_tokens(monkeypatch):
    watch = {}
    persisted = []

    async def fake_hydrate(session, chain_id, token_address):
        return [{"dexId": "pumpfun", "pairAddress": "pair-123"}]

    async def fake_persist_discovery(**kwargs):
        persisted.append(kwargs)

    monkeypatch.setattr(listener, "graduation_watch", watch)
    monkeypatch.setattr(listener, "hydrate_token", fake_hydrate)
    monkeypatch.setattr(listener, "persist_discovery", fake_persist_discovery)

    profile = {"chainId": "solana", "tokenAddress": "token-123"}
    asyncio.run(listener.handle_token_profile(object(), profile))

    assert persisted[0]["status"] == "watching"
    assert persisted[0]["token_profile"] == profile
    assert "token-123" in watch


def test_handle_token_profile_persists_direct_pumpswap_tokens_as_new(
    monkeypatch,
):
    watch = {}
    persisted = []

    async def fake_hydrate(session, chain_id, token_address):
        return [{"dexId": "pumpswap", "pairAddress": "pair-123"}]

    async def fake_persist_discovery(**kwargs):
        persisted.append(kwargs)

    monkeypatch.setattr(listener, "graduation_watch", watch)
    monkeypatch.setattr(listener, "hydrate_token", fake_hydrate)
    monkeypatch.setattr(listener, "persist_discovery", fake_persist_discovery)

    asyncio.run(
        listener.handle_token_profile(
            object(),
            {"chainId": "solana", "tokenAddress": "token-123"},
        )
    )

    assert persisted[0]["status"] == "new"
    assert watch == {}


def test_check_graduations_promotes_pumpswap_tokens(monkeypatch):
    watch = {
        "token-123": {
            "added_at": listener.now_utc(),
            "token_profile": {
                "chainId": "solana",
                "tokenAddress": "token-123",
            },
        }
    }
    persisted = []

    async def fake_hydrate(session, chain_id, token_address):
        return [{"dexId": "pumpswap", "pairAddress": "pair-456"}]

    async def fake_persist_discovery(**kwargs):
        persisted.append(kwargs)

    monkeypatch.setattr(listener, "graduation_watch", watch)
    monkeypatch.setattr(listener, "hydrate_token", fake_hydrate)
    monkeypatch.setattr(listener, "persist_discovery", fake_persist_discovery)

    asyncio.run(listener.check_graduations(object()))

    assert watch == {}
    assert persisted[0]["status"] == "graduated"
    assert persisted[0]["graduated_at"] is not None


def test_check_graduations_removes_expired_tokens_without_hydrating(
    monkeypatch,
):
    watch = {
        "token-123": {
            "added_at": listener.now_utc()
            - timedelta(seconds=listener.GRADUATION_EXPIRY_SECONDS + 1),
            "token_profile": {"tokenAddress": "token-123"},
        }
    }

    async def fail_if_hydrated(*args, **kwargs):
        raise AssertionError("expired token was hydrated")

    monkeypatch.setattr(listener, "graduation_watch", watch)
    monkeypatch.setattr(listener, "hydrate_token", fail_if_hydrated)

    asyncio.run(listener.check_graduations(object()))

    assert watch == {}


class FakeResponse:
    def __init__(self, status, payload=None, error=None):
        self.status = status
        self.payload = payload
        self.error = error

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None

    async def json(self):
        if self.error:
            raise self.error

        return self.payload


class FakeHttpSession:
    def __init__(self, response):
        self.response = response
        self.request = None

    def get(self, url, **kwargs):
        self.request = {"url": url, "kwargs": kwargs}
        return self.response


def test_hydrate_token_returns_pairs_from_successful_response():
    response = FakeResponse(200, [{"dexId": "pumpswap"}])
    session = FakeHttpSession(response)

    result = asyncio.run(
        listener.hydrate_token(session, "solana", "token-123")
    )

    assert result == [{"dexId": "pumpswap"}]
    assert session.request["url"].endswith("/solana/token-123")


def test_hydrate_token_returns_none_for_bad_http_or_payload():
    bad_responses = [
        FakeResponse(503, [{"dexId": "pumpswap"}]),
        FakeResponse(200, {"not": "a list"}),
        FakeResponse(200, error=ValueError("invalid JSON")),
    ]

    for response in bad_responses:
        result = asyncio.run(
            listener.hydrate_token(
                FakeHttpSession(response),
                "solana",
                "token-123",
            )
        )

        assert result is None


def test_persist_discovery_sync_maps_pair_data_to_service(monkeypatch):
    calls = []
    session = object()
    discovery = SimpleNamespace(
        id=1,
        symbol="EXAMPLE",
        exchange="pumpswap",
        status="new",
    )

    class FakeSessionContext:
        def __enter__(self):
            return session

        def __exit__(self, exc_type, exc_value, traceback):
            return None

    def fake_record_discovery(received_session, **kwargs):
        calls.append((received_session, kwargs))
        return discovery

    monkeypatch.setattr(listener, "SessionLocal", FakeSessionContext)
    monkeypatch.setattr(listener, "record_discovery", fake_record_discovery)

    listener.persist_discovery_sync(
        {"tokenAddress": "token-123"},
        {
            "pairAddress": "pair-123",
            "dexId": "PumpSwap",
            "baseToken": {
                "name": "Example Token",
                "symbol": "EXAMPLE",
            },
        },
        "new",
    )

    assert calls == [
        (
            session,
            {
                "token_address": "token-123",
                "pair_address": "pair-123",
                "name": "Example Token",
                "symbol": "EXAMPLE",
                "source": "DexScreener",
                "exchange": "pumpswap",
                "status": "new",
                "graduated_at": None,
            },
        )
    ]


def test_persist_discovery_sync_skips_profiles_without_token_address(
    monkeypatch,
):
    class UnexpectedSession:
        def __call__(self):
            raise AssertionError("database session should not be opened")

    monkeypatch.setattr(listener, "SessionLocal", UnexpectedSession())

    listener.persist_discovery_sync(
        {},
        {"pairAddress": "pair-123"},
        "new",
    )
