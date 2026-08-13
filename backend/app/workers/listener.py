import asyncio
import json
from datetime import datetime, timezone

import aiohttp
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError

from app.database.connection import SessionLocal
from app.services.discovery import record_discovery


WS_URL = "wss://api.dexscreener.com/token-profiles/latest/v1"
DEX_TOKEN_URL = (
    "https://api.dexscreener.com/tokens/v1/"
    "{chain_id}/{token_address}"
)

GRADUATION_POLL_SECONDS = 60
GRADUATION_EXPIRY_SECONDS = 3 * 60 * 60

# replace with DB persistence?
graduation_watch: dict[str, dict] = {}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


async def hydrate_token(
    session: aiohttp.ClientSession,
    chain_id: str,
    token_address: str,
) -> list[dict] | None:
    url = DEX_TOKEN_URL.format(
        chain_id=chain_id,
        token_address=token_address,
    )

    try:
        async with session.get(
            url,
            headers={"Accept": "*/*"},
            timeout=10,
        ) as response:
            if response.status != 200:
                print(
                    f"[hydrate] HTTP {response.status} "
                    f"for {token_address}"
                )
                return None

            data = await response.json()

            if not isinstance(data, list):
                return None

            return data

    except Exception as error:
        print(
            "[hydrate error]",
            type(error).__name__,
            error,
        )
        return None


def add_to_graduation_watch(
    token_address: str,
    token_profile: dict,
) -> None:
    if token_address in graduation_watch:
        return

    graduation_watch[token_address] = {
        "added_at": now_utc(),
        "token_profile": token_profile,
    }

    print(
        f"[graduation-watch] added {token_address}"
    )


def persist_discovery_sync(
    token_profile: dict,
    pair: dict,
    status: str,
    graduated_at: datetime | None = None,
) -> None:
    token_address = token_profile.get("tokenAddress")

    if not token_address:
        return

    base_token = pair.get("baseToken", {}) or {}

    with SessionLocal() as session:
        discovery = record_discovery(
            session,
            token_address=token_address,
            pair_address=pair.get("pairAddress"),
            name=base_token.get("name", ""),
            symbol=base_token.get("symbol", ""),
            source="DexScreener",
            exchange=str(
                pair.get("dexId", "")
            ).lower() or None,
            status=status,
            graduated_at=graduated_at,
        )

    print(
        f"[database] discovery id={discovery.id} "
        f"symbol={discovery.symbol} "
        f"exchange={discovery.exchange} "
        f"status={discovery.status}"
    )


async def persist_discovery(
    token_profile: dict,
    pair: dict,
    status: str,
    graduated_at: datetime | None = None,
) -> None:
    await asyncio.to_thread(
        persist_discovery_sync,
        token_profile,
        pair,
        status,
        graduated_at,
    )


async def handle_token_profile(
    session: aiohttp.ClientSession,
    token_profile: dict,
) -> None:
    chain_id = token_profile.get("chainId")
    token_address = token_profile.get("tokenAddress")

    if chain_id != "solana":
        return

    if not token_address:
        return

    print(
        f"[profile] Solana token found: "
        f"{token_address}"
    )

    pairs = await hydrate_token(
        session,
        chain_id,
        token_address,
    )

    if not pairs:
        return

    for pair in pairs:
        dex_id = str(
            pair.get("dexId", "")
        ).lower()

        if dex_id == "pumpfun":
            await persist_discovery(
                token_profile=token_profile,
                pair=pair,
                status="watching",
            )

            add_to_graduation_watch(
                token_address,
                token_profile,
            )

        elif dex_id in {
            "pumpswap",
            "raydium",
        }:
            await persist_discovery(
                token_profile=token_profile,
                pair=pair,
                status="new",
            )

            return


async def check_graduations(
    session: aiohttp.ClientSession,
) -> None:
    current_time = now_utc()
    to_remove: list[str] = []

    for token_address, info in list(
        graduation_watch.items()
    ):
        age_seconds = (
            current_time - info["added_at"]
        ).total_seconds()

        if age_seconds > GRADUATION_EXPIRY_SECONDS:
            print(
                f"[graduation-watch] expired "
                f"{token_address}"
            )

            to_remove.append(token_address)
            continue

        pairs = await hydrate_token(
            session,
            "solana",
            token_address,
        )

        if not pairs:
            continue

        for pair in pairs:
            dex_id = str(
                pair.get("dexId", "")
            ).lower()

            if dex_id != "pumpswap":
                continue

            print(
                f"[graduated] {token_address}"
            )

            await persist_discovery(
                token_profile=info["token_profile"],
                pair=pair,
                status="graduated",
                graduated_at=now_utc(),
            )

            to_remove.append(token_address)
            break

    for token_address in to_remove:
        graduation_watch.pop(
            token_address,
            None,
        )


async def graduation_poll_loop(
    session: aiohttp.ClientSession,
) -> None:
    while True:
        try:
            if graduation_watch:
                print(
                    "[graduation-watch] checking "
                    f"{len(graduation_watch)} tokens"
                )

                await check_graduations(session)

        except Exception as error:
            print(
                "[graduation-loop error]",
                type(error).__name__,
                error,
            )

        await asyncio.sleep(
            GRADUATION_POLL_SECONDS
        )


async def listen_once() -> None:
    async with aiohttp.ClientSession() as session:
        graduation_task = asyncio.create_task(
            graduation_poll_loop(session)
        )

        try:
            async with websockets.connect(
                WS_URL,
                ping_interval=20,
                ping_timeout=20,
                close_timeout=5,
            ) as websocket:
                print(
                    "[discoverer] connected to DexScreener"
                )

                while True:
                    message = await websocket.recv()

                    if not message:
                        continue

                    try:
                        data = json.loads(message)

                    except json.JSONDecodeError:
                        continue

                    if isinstance(data, dict):
                        message_type = str(
                            data.get("type", "")
                        ).lower()

                        if message_type in {
                            "heartbeat",
                            "ping",
                            "pong",
                        }:
                            continue

                        data = [data]

                    if not isinstance(data, list):
                        continue

                    for token_profile in data:
                        if not isinstance(
                            token_profile,
                            dict,
                        ):
                            continue

                        await handle_token_profile(
                            session,
                            token_profile,
                        )

        finally:
            graduation_task.cancel()

            try:
                await graduation_task
            except asyncio.CancelledError:
                pass


async def main() -> None:
    reconnect_delay = 1

    while True:
        try:
            await listen_once()

            reconnect_delay = 1

        except (
            ConnectionClosed,
            ConnectionClosedError,
        ) as error:
            print(
                f"[ws closed] {error}. "
                f"reconnecting in "
                f"{reconnect_delay}s..."
            )

        except Exception as error:
            print(
                f"[ws error] "
                f"{type(error).__name__}: "
                f"{error}. reconnecting in "
                f"{reconnect_delay}s..."
            )

        await asyncio.sleep(reconnect_delay)

        reconnect_delay = min(
            reconnect_delay * 2,
            30,
        )


if __name__ == "__main__":
    asyncio.run(main())