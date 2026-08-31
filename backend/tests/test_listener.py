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
