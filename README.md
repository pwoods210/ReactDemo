# TerMEMEal

TerMEMEal is a containerized Solana token-discovery dashboard. It consumes token-profile events from DexScreener, enriches them with pair data, tracks a small token lifecycle, stores discoveries in PostgreSQL, and presents them in a React dashboard.

The trade panel is a paper-mode interface only. The application does not collect wallet information or execute trades.

## Features

- Live Solana token-profile ingestion from DexScreener
- REST hydration of token metadata and pair data
- Pump.fun, PumpSwap, and Raydium classification
- Pump.fun graduation monitoring
- PostgreSQL persistence with conflict-safe upserts
- Protection against downgrading graduated tokens
- Enriched token cards with images and five-minute price changes
- Persistent discovery dismissal with animated feed replacement
- Client-side review badges and retention of watched cards in the feed
- API, listener, database, and trade-service status display
- Five-second frontend polling
- Docker Compose development environment
- Backend, frontend, and PostgreSQL integration tests
- GitHub Actions checks for tests, linting, and production builds

## Architecture

```text
DexScreener WebSocket
          │ token profiles
          ▼
  listener worker ─── REST hydration ───► DexScreener API
          │
          │ discovery upserts
          ▼
     PostgreSQL ◄──────── FastAPI ◄──────── React frontend
                              ▲                 polling
                              │ heartbeat
                         listener worker
```

The API and listener run as separate processes and share the backend code and PostgreSQL database. The frontend communicates only with FastAPI; it does not connect directly to DexScreener or PostgreSQL.

## Technology stack

| Area | Technologies |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, TanStack Query, Bootstrap, CSS |
| Backend | Python 3.12, FastAPI, Pydantic Settings, SQLAlchemy, psycopg |
| Worker | asyncio, aiohttp, websockets |
| Database | PostgreSQL 18, Alembic |
| Testing | pytest, Vitest, Testing Library, jsdom |
| Tooling | Docker, Docker Compose, oxlint, GitHub Actions |

## Runtime components

### Frontend

The Vite application includes:

- `FaceGate`: displays the content warning before the dashboard is entered
- `Header`: shows branding, wallet state, and service health
- `DiscoveryFeed`: polls discoveries, manages dismissal, and preserves locally watched cards
- `TokenCard`: displays token metadata, imagery, price movement, and a review badge
- `DiscoveryScroll`: provides pointer and keyboard controls for the horizontal feed
- `TradePanel`: presents the non-functional paper-mode trade form

TanStack Query owns server state. The discovery feed and service-health query each refresh every five seconds. Feed position is saved in browser local storage.

The card badge cycles through `new`, `watching`, and `seen`. This is temporary browser state and is separate from the backend token lifecycle status.

### FastAPI API

FastAPI creates database sessions through SQLAlchemy, delegates discovery operations to the service and repository layers, and serializes database fields into the frontend's camelCase contract.

### Listener

`backend/app/workers/listener.py` runs as a long-lived process:

1. Connect to DexScreener's token-profile WebSocket.
2. Ignore non-Solana profiles and profiles without a token address.
3. Hydrate accepted addresses through DexScreener's token REST endpoint.
4. Classify supported pairs by `dexId`.
5. Persist PumpSwap and Raydium discoveries as `new`.
6. Persist Pump.fun discoveries as `watching` and add them to an in-memory graduation watch.
7. Poll watched tokens every 60 seconds. Tokens that acquire a PumpSwap pair become `graduated`; watches older than three hours expire.
8. Send a heartbeat to the API every five seconds and reconnect with exponential backoff after WebSocket failures.

The listener uses `asyncio` for network work and sends synchronous database persistence to a worker thread.

## Discovery lifecycle and data

Backend lifecycle statuses are:

| Status | Meaning |
| --- | --- |
| `new` | A supported PumpSwap or Raydium pair was discovered |
| `watching` | A Pump.fun token is being monitored for graduation |
| `graduated` | A monitored token later acquired a PumpSwap pair |

The `discoveries` table stores:

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `token_address` | Unique Solana token address |
| `pair_address` | Pair address, when available |
| `name`, `symbol` | Display metadata from the hydrated pair |
| `source` | Discovery provider, currently `DexScreener` |
| `exchange` | Normalized DEX identifier |
| `token_profile` | Original DexScreener profile payload |
| `pairs_data` | Complete hydrated pair response |
| `status` | Backend lifecycle status |
| `discovered_at` | Database creation time |
| `graduated_at` | PumpSwap promotion time, when applicable |
| `dismissed_at` | Time the user dismissed the discovery |

Upserts are keyed by `token_address`, so repeated events update one record instead of creating duplicates. A graduated record cannot be downgraded by a later event. The API returns up to 50 non-dismissed discoveries, newest first.

## API

Local API URL: `http://localhost:8000`

Interactive documentation: `http://localhost:8000/docs`

### `GET /api/discoveries`

Returns the active discovery feed:

```json
[
  {
    "id": 12,
    "name": "Example Token",
    "symbol": "EXAMPLE",
    "tokenAddress": "ExampleSolanaAddress",
    "pairAddress": "ExamplePairAddress",
    "source": "DexScreener",
    "exchange": "pumpswap",
    "discoveredAt": "2026-08-31T17:00:00Z",
    "status": "watching",
    "graduatedAt": null,
    "tokenProfile": {
      "chainId": "solana",
      "tokenAddress": "ExampleSolanaAddress",
      "icon": "https://example.com/icon.png"
    },
    "pairs": [
      {
        "chainId": "solana",
        "dexId": "pumpswap",
        "pairAddress": "ExamplePairAddress",
        "priceUsd": "1.25",
        "liquidity": {"usd": 1000}
      }
    ]
  }
]
```

### `POST /api/discoveries/{discovery_id}/dismiss`

Sets the discovery's `dismissed_at` timestamp. Successful requests return `204 No Content`; unknown IDs return `404 Not Found`. Dismissed discoveries are excluded from subsequent feed requests.

### `GET /health/api`

Returns `true` when the FastAPI process responds.

### `GET /health/services`

Reports the API's view of the listener, database, and trade service:

```json
{
  "discovery": {"status": "up"},
  "trade": {"status": "down"},
  "database": {"status": "up"}
}
```

The trade service is intentionally reported as down because no trade backend exists. Listener health is based on the most recent in-memory heartbeat.

### `POST /health/discovery/heartbeat`

Records a listener heartbeat and returns `{"ok": true}`.

## Quick start

Requirements: Docker Desktop with Compose and Git.

From the repository root:

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec api python -m alembic upgrade head
```

Open:

- Frontend: `http://localhost:5173`
- API documentation: `http://localhost:8000/docs`
- API health: `http://localhost:8000/health/api`

Migrations are explicit; the API image does not apply them automatically. Database records persist in the `postgres_data` volume across restarts.

Useful commands:

```bash
docker compose ps
docker compose logs -f listener
docker compose logs -f api
docker compose down
```

To intentionally remove containers and persisted database volumes, run `docker compose down -v`.

## Configuration

Copy the environment template before starting Compose:

```bash
cp .env.example .env
```

The template defines:

```env
APP_NAME=TerMEMEal API
APP_VERSION=0.1.0
FRONTEND_ORIGIN=http://localhost:5173
POSTGRES_DB=meme_trade
POSTGRES_USER=meme_trade
POSTGRES_PASSWORD=change-me
DATABASE_URL=postgresql+psycopg://meme_trade:change-me@db:5432/meme_trade
```

Do not commit production credentials in `.env`. The listener's provider URLs, internal API URL, and polling intervals are currently constants in `backend/app/workers/listener.py`. Frontend API URLs are also configured directly in the frontend API modules.

## Tests and checks

All checks can run through Docker; host Python and Node installations are not required.

### Backend unit and API tests

```bash
docker build -f backend/Dockerfile.test -t turmemeal-backend-test backend
docker run --rm turmemeal-backend-test
```

The default test image excludes tests marked `integration`.

### PostgreSQL integration tests

```bash
docker compose --profile test run --build --rm test pytest -m integration
```

Integration tests use the separate `db-test` service and `${POSTGRES_DB}_test` database. They do not use the development database.

### Frontend tests, lint, and build

```bash
docker build -f frontend/Dockerfile.test -t turmemeal-frontend-test frontend
docker run --rm turmemeal-frontend-test
docker run --rm turmemeal-frontend-test npm run lint
docker run --rm turmemeal-frontend-test npm run build
```

Frontend tests use Vitest, jsdom, and Testing Library. They cover API clients, feed states, dismissal, watched-card retention, token-card behavior, and the content-warning gate.

The GitHub Actions workflow runs backend unit tests, PostgreSQL integration tests, frontend tests, oxlint, and the production frontend build for pushes and pull requests targeting `main`.

## Database migrations

Alembic migrations live in `backend/alembic/versions/`. After changing a SQLAlchemy model:

```bash
docker compose exec api python -m alembic revision --autogenerate -m "describe change"
docker compose exec api python -m alembic upgrade head
```

Review autogenerated migrations before committing them. Migrations change schema only; they are not data backups.

## Repository layout

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             FastAPI routes
│   │   ├── database/        Engine, models, and repository
│   │   ├── schemas/         Pydantic API schemas
│   │   ├── services/        Application operations
│   │   └── workers/         DexScreener listener
│   ├── alembic/             Database migrations
│   ├── tests/               Unit, API, and integration tests
│   ├── Dockerfile           API and listener runtime image
│   └── Dockerfile.test      Backend test image
├── frontend/
│   ├── src/api/             API clients and tests
│   ├── src/Components/      React components and tests
│   ├── Dockerfile           Vite development image
│   └── Dockerfile.test      Frontend test image
├── .github/workflows/       GitHub Actions workflow
├── compose.yml              Development and test services
└── .env.example             Local configuration template
```

## Known limitations

- The graduation watch is held in listener memory. Restarting the listener loses pending watches, although persisted discoveries remain.
- User-selected card review badges are local component state and are not persisted.
- Listener heartbeats are stored in API memory and disappear when the API restarts.
- Provider retry handling is limited to WebSocket reconnect backoff; explicit rate-limit handling is not implemented.
- The frontend polls rather than receiving pushed updates.
- API and provider URLs are not fully environment-configurable.
- Authentication, authorization, and multi-user state are not implemented.
- There is no browser-level full-stack test.
- The trade form is presentational and the wallet indicator is always disconnected.
- The current configuration targets local Compose development, not production deployment.

## Next steps

The highest-value improvements are durable listener recovery, environment-based worker and frontend configuration, stronger provider retry handling, and a browser-level full-stack test. Real trading should remain a separate security-sensitive feature rather than being implied by the current interface.
