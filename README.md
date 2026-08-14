# TerMEMEal

TerMEMEal is a full-stack, containerized Solana token discovery and trading dashboard.

The application continuously listens for new Solana token profiles, tracks token lifecycle events such as Pump.fun graduations, persists discoveries to PostgreSQL, exposes discovery data through a FastAPI REST API, and renders the resulting token feed in a React dashboard.

The project is designed around independently deployable services and a clear separation between:

- frontend presentation
- HTTP API
- background discovery workers
- application services
- database persistence
- external data providers

The current application focuses primarily on the **token discovery pipeline and dashboard infrastructure**. Trading controls and additional real-time functionality are being built on top of this foundation.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Current Project Status](#current-project-status)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Languages](#languages)
- [Frontend](#frontend)
- [Backend](#backend)
- [Background Workers](#background-workers)
- [Database](#database)
- [External Services](#external-services)
- [Application Features](#application-features)
- [Token Discovery Lifecycle](#token-discovery-lifecycle)
- [API](#api)
- [Database Model](#database-model)
- [Project Structure](#project-structure)
- [Docker Services](#docker-services)
- [Configuration](#configuration)
- [Local Development](#local-development)
- [Common Development Commands](#common-development-commands)
- [Database Migrations](#database-migrations)
- [Frontend Data Flow](#frontend-data-flow)
- [Persistence](#persistence)
- [Reliability and Recovery](#reliability-and-recovery)
- [Current Limitations](#current-limitations)
- [Planned Features](#planned-features)
- [Architecture Principles](#architecture-principles)

---

# Project Overview

TerMEMEal currently implements an end-to-end token discovery pipeline:

```text
DexScreener
     │
     │ WebSocket / REST
     ▼
Discovery Listener
     │
     │ application service
     ▼
PostgreSQL
     │
     │ SQLAlchemy
     ▼
FastAPI
     │
     │ REST
     ▼
TanStack Query
     │
     ▼
React Dashboard
```

The discovery listener runs independently from the FastAPI server.

This allows the application to continuously collect token information regardless of whether a browser is connected to the frontend.

PostgreSQL acts as the system of record between the worker and API.

The frontend therefore does not communicate directly with the discovery listener.

Instead:

```text
Discovery Worker
       │
       ▼
   PostgreSQL
       ▲
       │
   FastAPI API
       ▲
       │
 React Frontend
```

This separation allows each component to eventually scale and deploy independently.

---

# Current Project Status

The following functionality is currently implemented.

### Working

- React frontend
- TypeScript frontend codebase
- Bootstrap-based responsive UI
- custom dark dashboard theme
- FastAPI backend
- Dockerized frontend
- Dockerized FastAPI backend
- Dockerized discovery worker
- Dockerized PostgreSQL database
- Docker Compose orchestration
- PostgreSQL persistence
- Alembic database migrations
- SQLAlchemy ORM
- DexScreener WebSocket listener
- Solana-only discovery filtering
- DexScreener token hydration
- Pump.fun detection
- PumpSwap detection
- Raydium detection
- Pump.fun graduation monitoring
- database discovery upserts
- persistent token lifecycle status
- REST discovery endpoint
- frontend polling through TanStack Query
- automatic React rerendering when backend data changes
- horizontal token discovery feed
- custom discovery feed scroll control
- auto-follow behavior for newly discovered tokens
- persistent database state between container restarts

### Partially implemented / UI only

- trade panel
- buy button
- sell button
- SOL amount input
- slippage input
- timed auto-sell configuration
- wallet connection display
- paper trading mode

### Planned

- actual transaction execution
- wallet integration
- SSE live event streaming
- discovery dismissal
- historical transaction storage
- trading history
- listener state restoration
- market data enrichment
- trade monitoring
- deployment to AWS
- production authentication / authorization
- production observability

---

# Architecture

TerMEMEal follows a service-oriented architecture within a single repository.

```text
                     ┌─────────────────────┐
                     │     DexScreener     │
                     └──────────┬──────────┘
                                │
                       WebSocket / REST
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Discovery Listener  │
                     │      Worker         │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Discovery Service   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    Repository       │
                     │     SQLAlchemy      │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     PostgreSQL      │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      FastAPI        │
                     │       REST API      │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   TanStack Query    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │       React         │
                     │      Dashboard      │
                     └─────────────────────┘
```

---

# Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| React | Component-based frontend UI |
| TypeScript | Static typing for frontend JavaScript |
| TSX | React component implementation |
| Vite | Frontend build tooling and development server |
| TanStack Query | Server-state fetching, caching, and refetching |
| Bootstrap | Layout, responsive utilities, forms, and UI primitives |
| CSS | Custom dashboard styling and animations |
| HTML5 | Application markup |
| Oxlint | Frontend linting |
| Fetch API | HTTP communication with FastAPI |

---

## Backend

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend application language |
| FastAPI | HTTP REST API |
| Uvicorn | ASGI application server |
| Pydantic | API models and validation |
| Pydantic Settings | Environment-based configuration |
| SQLAlchemy | ORM and database access |
| psycopg | PostgreSQL Python driver |
| Alembic | Database schema migrations |
| asyncio | Asynchronous worker execution |
| aiohttp | Asynchronous HTTP requests |
| websockets | DexScreener WebSocket connection |

---

## Database

| Technology | Purpose |
|---|---|
| PostgreSQL 18 | Persistent relational database |
| SQLAlchemy ORM | Python database models and queries |
| Alembic | Schema versioning |
| Docker named volumes | Local database persistence |

---

## Infrastructure / Tooling

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Local multi-service orchestration |
| Git | Source control |
| GitHub | Remote repository / collaboration |
| Node.js 22 | Frontend development environment |
| npm | JavaScript dependency management |

---

# Languages

The project currently uses several languages and configuration formats.

### TypeScript

Used throughout the React frontend.

```text
.ts
.tsx
```

TypeScript provides compile-time checking for:

- API response objects
- React component props
- token discovery models
- application state
- utility functions

---

### Python

Used throughout the backend.

Python currently powers:

- FastAPI
- SQLAlchemy
- PostgreSQL interaction
- DexScreener WebSocket handling
- asynchronous discovery processing
- token lifecycle tracking

---

### SQL

PostgreSQL performs persistent storage for:

- token discoveries
- lifecycle state
- exchange information
- timestamps

SQL is primarily generated through SQLAlchemy, although manual SQL may also be used for development and inspection.

---

### CSS

Custom CSS provides the dashboard visual design beyond Bootstrap defaults.

This includes:

- dark surfaces
- token cards
- discovery feed layout
- horizontal scrolling
- custom scroll control
- responsive behavior
- status styling
- edge fade effects

---

### YAML

Used for Docker Compose configuration.

```text
compose.yaml
```

---

### Dockerfile

Dockerfiles define container environments for:

- frontend
- backend

---

### Environment configuration

Runtime configuration uses `.env` files.

```text
.env
.env.example
```

---

# Frontend

The frontend is a React application built with Vite and TypeScript.

Its current role is to provide a live dashboard for viewing discovered tokens and eventually interacting with the trading backend.

---

## Main frontend responsibilities

The frontend is responsible for:

- displaying token discoveries
- displaying token lifecycle status
- requesting data from the backend
- caching server state
- periodically refreshing discovery data
- providing token scrolling controls
- displaying trading controls
- presenting application status

The frontend **does not communicate directly with PostgreSQL or DexScreener**.

All backend data flows through FastAPI.

---

## Discovery Feed

The discovery feed displays tokens as horizontally scrolling cards.

```text
oldest                                      newest
   ↓                                           ↓

[ TOKEN ] [ TOKEN ] [ TOKEN ] [ TOKEN ] [ TOKEN ]
```

New discoveries are added to the right side of the feed.

The feed supports:

- horizontal scrolling
- trackpad / touch scrolling
- custom joystick-style scroll control
- keyboard scrolling
- hidden native scrollbar
- automatic scrolling when following live discoveries
- preserving scroll location while examining older discoveries

---

## Auto-follow behavior

The discovery feed tracks whether the user is currently at the newest/rightmost position.

If the user is already viewing the newest discoveries:

```text
[A] [B] [C]
         ↑
```

and token `D` arrives:

```text
[A] [B] [C] [D]
             ↑
```

the feed automatically scrolls to the new card.

If the user has intentionally scrolled backward:

```text
[A] [B] [C]
 ↑
```

a new discovery does **not** force the feed back to the newest position.

This allows users to inspect older tokens without fighting automatic scrolling.

---

## Custom Scroll Control

The feed includes a joystick / lever-style horizontal controller.

The control uses:

- React refs
- Pointer Events
- pointer capture
- `requestAnimationFrame`
- direct `scrollLeft` manipulation
- keyboard controls

The lever supports variable scroll velocity depending on how far the user drags it from the center.

---

## Discovery Feed Viewport

Token cards are displayed inside an inset discovery viewport inside the larger Live Discovery panel.

The viewport visually separates the scrolling card area from the outer dashboard container.

Edge gradient overlays create a fade effect where cards enter and exit the visible viewport.

This allows cards to visually disappear into the container rather than abruptly clipping at its edge.

---

## TanStack Query

TanStack Query manages backend server state.

The discovery feed currently performs:

```text
GET /api/discoveries
```

approximately every five seconds.

TanStack Query handles:

- request lifecycle
- cached discovery data
- loading state
- error state
- background refetching
- automatic React updates

The application intentionally separates:

```text
React local UI state
```

from:

```text
server state
```

Local UI state uses normal React primitives such as `useState` and `useRef`.

Remote backend state is managed by TanStack Query.

---

# Backend

The backend is built with FastAPI.

FastAPI provides the HTTP interface between the React application and the backend application logic.

The backend is intentionally divided into several layers.

```text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

---

# API Layer

Located under:

```text
backend/app/api/
```

API modules define HTTP routes.

Examples:

```text
api/
├── discoveries.py
└── health.py
```

The API layer is responsible for:

- HTTP routing
- dependency injection
- request parsing
- response serialization
- HTTP response codes

The API layer should contain minimal application logic.

---

# Service Layer

Located under:

```text
backend/app/services/
```

For example:

```text
services/discovery.py
```

The service layer represents application operations.

Current discovery service responsibilities include operations such as:

```text
get_recent_discoveries()
record_discovery()
```

The service layer separates domain/application behavior from HTTP and database implementation details.

This allows the same service logic to be called from:

```text
FastAPI
```

and:

```text
background workers
```

without duplicating behavior.

---

# Repository Layer

Located under:

```text
backend/app/database/repositories/
```

Repositories contain database-specific queries and persistence operations.

For example:

```text
database/repositories/discovery.py
```

Responsibilities include:

- selecting discoveries
- inserting discoveries
- updating discoveries
- PostgreSQL upserts
- filtering dismissed discoveries
- ordering results

This keeps SQLAlchemy-specific behavior out of the API layer.

---

# Background Workers

Long-running background processes live under:

```text
backend/app/workers/
```

The main current worker is:

```text
workers/listener.py
```

Unlike FastAPI, this process is not started in response to HTTP requests.

It runs continuously.

---

## Discovery Listener

The discovery listener connects to DexScreener's WebSocket feed.

The listener performs:

1. WebSocket connection
2. incoming message parsing
3. heartbeat filtering
4. Solana filtering
5. token-address hydration
6. exchange classification
7. discovery persistence
8. Pump.fun lifecycle monitoring
9. PumpSwap graduation detection
10. WebSocket reconnection

---

## WebSocket Reconnection

The listener includes automatic reconnection logic.

If the DexScreener WebSocket closes or fails:

```text
connection lost
      ↓
wait
      ↓
reconnect
```

The reconnect delay increases up to a maximum delay rather than immediately retrying continuously.

This prevents rapid connection loops during external service outages.

---

# External Services

## DexScreener

DexScreener is currently the primary token discovery provider.

The project uses:

### WebSocket

Used for receiving newly published token profiles.

### REST API

Used to hydrate a token address and retrieve available trading pairs.

Hydration provides information such as:

- pair address
- DEX
- token name
- token symbol
- pair URL
- token pair metadata

---

# Supported Exchanges / Sources

The listener currently recognizes:

### Pump.fun

```text
dexId = pumpfun
```

Pump.fun discoveries are persisted immediately and placed into graduation monitoring.

Initial state:

```text
exchange = pumpfun
status = watching
```

---

### PumpSwap

```text
dexId = pumpswap
```

Direct PumpSwap discoveries are stored immediately.

A PumpSwap pair can also represent a Pump.fun token that has graduated.

---

### Raydium

```text
dexId = raydium
```

Raydium discoveries are currently accepted as direct discoveries.

---

# Application Features

## Live token discovery

The backend continuously receives new Solana token profiles without requiring browser activity.

---

## Persistent discovery history

Discoveries are stored in PostgreSQL.

This means discovery history survives:

- page refreshes
- frontend restarts
- backend restarts
- listener restarts
- Docker container recreation

---

## Token lifecycle tracking

A token can change state over time.

Example:

```text
Pump.fun detected
      ↓
WATCHING
      ↓
PumpSwap detected
      ↓
GRADUATED
```

Instead of inserting an entirely new token when graduation occurs, the existing database row is updated.

---

## Database upserts

Token address is used as a unique token identifier.

The database persistence operation behaves conceptually as:

```text
token does not exist
        ↓
      INSERT

token already exists
        ↓
      UPDATE
```

This prevents duplicate discovery rows while allowing token lifecycle information to evolve.

---

## Live React updates

The frontend currently polls FastAPI every five seconds.

When PostgreSQL changes:

```text
PostgreSQL
     ↓
FastAPI
     ↓
TanStack Query
     ↓
React rerender
```

No browser refresh is necessary.

---

## Status-based cards

Token cards can display lifecycle states such as:

```text
NEW
WATCHING
GRADUATED
```

For example:

```text
┌──────────────────────────────┐
│ DOGE2                 WATCHING
│                              │
│ Pump.fun                     │
│                              │
│ Address: 8x...pump           │
└──────────────────────────────┘
```

After graduation:

```text
┌──────────────────────────────┐
│ DOGE2               GRADUATED
│                              │
│ PumpSwap                     │
│                              │
│ Address: 8x...pump           │
└──────────────────────────────┘
```

The same React card identity can remain because the database `id` remains unchanged.

---

# Token Discovery Lifecycle

## Direct PumpSwap discovery

```text
DexScreener profile
       ↓
Solana?
       ↓
hydrate token
       ↓
PumpSwap pair
       ↓
record discovery
       ↓
PostgreSQL
       ↓
FastAPI
       ↓
React
```

---

## Direct Raydium discovery

```text
DexScreener profile
       ↓
Solana?
       ↓
hydrate token
       ↓
Raydium pair
       ↓
record discovery
       ↓
PostgreSQL
       ↓
React
```

---

## Pump.fun discovery

Pump.fun has a longer lifecycle.

```text
DexScreener
     ↓
Pump.fun detected
     ↓
write database row
     ↓
status = watching
     ↓
add token to graduation watch
     ↓
poll DexScreener periodically
     ↓
PumpSwap pair detected
     ↓
update database row
     ↓
status = graduated
exchange = pumpswap
graduated_at = timestamp
     ↓
React rerenders card
```

---

# API

FastAPI currently provides the application's REST API.

Local development URL:

```text
http://localhost:8000
```

Interactive OpenAPI documentation:

```text
http://localhost:8000/docs
```

---

## Health

### `GET /health`

Basic API health endpoint.

Example response:

```json
{
  "status": "ok"
}
```

This currently confirms that the FastAPI application is running.

---

## Discoveries

### `GET /api/discoveries`

Returns active token discoveries.

Example response:

```json
[
  {
    "id": 12,
    "name": "Example Token",
    "symbol": "EXAMPLE",
    "tokenAddress": "ExampleSolanaAddress",
    "source": "DexScreener",
    "discoveredAt": "2026-08-14T17:00:00Z",
    "status": "watching"
  }
]
```

Results are retrieved through:

```text
API route
   ↓
Discovery Service
   ↓
Discovery Repository
   ↓
PostgreSQL
```

---

# Planned API Endpoints

The following are architectural plans and are **not necessarily implemented yet**.

### Discovery dismissal

```text
PATCH /api/discoveries/{id}/dismiss
```

Expected behavior:

```text
React
 ↓
TanStack Mutation
 ↓
FastAPI
 ↓
Discovery Service
 ↓
UPDATE dismissed_at
```

---

### Discovery event stream

```text
GET /api/discoveries/stream
```

Planned to use Server-Sent Events.

This would replace or supplement the current five-second frontend polling.

---

### Trading API

Future endpoints may support:

- buy
- sell
- timed sell
- transaction status
- transaction history

These are not part of the current production path.

---

# Database

PostgreSQL is the application's persistent system of record.

The database is not simply being used as a message transport mechanism.

It provides:

- persistence
- lifecycle state
- deduplication
- historical data
- queryability
- process independence
- restart recovery

---

# Database Model

The current discovery model contains fields similar to:

```text
discoveries
───────────────────────────────

id
token_address
pair_address
name
symbol
source
exchange
status
discovered_at
graduated_at
dismissed_at
```

---

## `id`

Internal database primary key.

Used by the frontend as a stable React identity.

---

## `token_address`

Solana token address.

This is unique and is used for discovery upserts.

---

## `pair_address`

Address of the trading pair.

This may initially be unavailable or may change when a Pump.fun token graduates.

---

## `name`

Token name.

---

## `symbol`

Token ticker symbol.

---

## `source`

Discovery source.

Currently generally:

```text
DexScreener
```

---

## `exchange`

Current detected exchange.

Examples:

```text
pumpfun
pumpswap
raydium
```

---

## `status`

Application lifecycle state.

Current states include:

```text
new
watching
graduated
```

---

## `discovered_at`

Timestamp representing when the token discovery was first persisted.

---

## `graduated_at`

Timestamp representing Pump.fun → PumpSwap graduation.

May be `NULL`.

---

## `dismissed_at`

Reserved for soft dismissal / archival behavior.

Instead of deleting discovery history, the application can eventually set:

```text
dismissed_at = timestamp
```

and exclude the discovery from the normal frontend feed.

---

# Project Structure

The repository is organized as a monorepo.

```text
TerMEMEal/
│
├── frontend/
│   │
│   ├── src/
│   │   ├── api/
│   │   │   └── discoveries.ts
│   │   │
│   │   ├── features/
│   │   │   └── discovery/
│   │   │       └── types.ts
│   │   │
│   │   ├── Components/
│   │   │   ├── DiscoveryFeed.tsx
│   │   │   ├── DiscoveryScrollControl.tsx
│   │   │   ├── TokenCard.tsx
│   │   │   └── ...
│   │   │
│   │   ├── App.tsx
│   │   ├── app.css
│   │   ├── index.css
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── discoveries.py
│   │   │   └── health.py
│   │   │
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   │
│   │   │   ├── models/
│   │   │   │   └── discovery.py
│   │   │   │
│   │   │   └── repositories/
│   │   │       └── discovery.py
│   │   │
│   │   ├── schemas/
│   │   │   └── discovery.py
│   │   │
│   │   ├── services/
│   │   │   └── discovery.py
│   │   │
│   │   ├── workers/
│   │   │   └── listener.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
│
├── compose.yaml
├── .env
├── .env.example
├── .gitignore
├── .gitattributes
└── README.md
```

The exact frontend component list may grow as additional dashboard features are added.

---

# Docker Services

Docker Compose currently coordinates four major services.

```text
frontend
api
listener
db
```

---

## `frontend`

Runs the Vite development server.

Typical local port:

```text
5173
```

Responsibilities:

- serve React development application
- provide HMR
- compile TypeScript / TSX
- communicate with FastAPI

---

## `api`

Runs FastAPI through Uvicorn.

Typical local port:

```text
8000
```

Responsibilities:

- expose REST endpoints
- validate API data
- query PostgreSQL
- return discovery information to frontend

---

## `listener`

Runs:

```text
python -m app.workers.listener
```

Responsibilities:

- connect to DexScreener
- monitor new profiles
- track Pump.fun graduations
- persist discoveries

The listener exposes no HTTP port.

---

## `db`

Runs PostgreSQL.

Responsibilities:

- persist discoveries
- maintain application state
- provide shared storage between worker and API

The API and listener connect to PostgreSQL over Docker's internal network using the Compose service hostname:

```text
db
```

---

# Shared Backend Image

The API and listener intentionally use the same backend image.

They run different commands:

```text
API
└── uvicorn app.main:app ...
```

```text
Listener
└── python -m app.workers.listener
```

This allows both processes to reuse:

- SQLAlchemy models
- repositories
- application services
- configuration
- Python dependencies

without maintaining two backend codebases.

---

# Configuration

Application configuration is supplied through environment variables.

Example `.env`:

```env
APP_NAME=TerMEMEal API
APP_VERSION=0.1.0
FRONTEND_ORIGIN=http://localhost:5173

POSTGRES_DB=meme_trade
POSTGRES_USER=meme_trade
POSTGRES_PASSWORD=meme_trade_dev

DATABASE_URL=postgresql+psycopg://meme_trade:meme_trade_dev@db:5432/meme_trade
```

Do not commit production credentials.

A sanitized template should be maintained in:

```text
.env.example
```

Example:

```env
APP_NAME=TerMEMEal API
APP_VERSION=0.1.0
FRONTEND_ORIGIN=http://localhost:5173

POSTGRES_DB=meme_trade
POSTGRES_USER=meme_trade
POSTGRES_PASSWORD=change-me

DATABASE_URL=postgresql+psycopg://meme_trade:change-me@db:5432/meme_trade
```

---

# Local Development

## Requirements

Install:

- Docker Desktop
- Docker Compose
- Git

Because the application runs inside containers, local installations of Python, PostgreSQL, and Node are generally not required to run the full stack.

---

## Start the application

From the repository root:

```powershell
docker compose up --build
```

Expected services:

```text
frontend
api
listener
db
```

---

## Run in the background

```powershell
docker compose up --build -d
```

---

## View service status

```powershell
docker compose ps
```

---

## View all logs

```powershell
docker compose logs -f
```

---

## View listener logs

```powershell
docker compose logs -f listener
```

Expected output may resemble:

```text
[discoverer] connected to DexScreener
[profile] Solana token found: ...
[database] discovery id=...
[graduation-watch] added ...
```

---

## View API logs

```powershell
docker compose logs -f api
```

---

## Stop containers

```powershell
docker compose down
```

This removes containers while keeping the PostgreSQL volume.

---

# Persistence

Normal shutdown:

```powershell
docker compose down
```

does **not** delete PostgreSQL data.

The database is stored in a Docker named volume.

Therefore:

```text
docker compose down
docker compose up
```

retains previous token discoveries.

---

## Delete development database

Be careful with:

```powershell
docker compose down -v
```

The `-v` option removes Compose-managed volumes.

That means the PostgreSQL development database will be deleted.

---

# Common Development Commands

## Rebuild backend

Use this when Python dependencies change:

```powershell
docker compose build api
```

Because the API and listener share the backend image, rebuilding the backend makes new dependencies available to both processes.

---

## Rebuild full application

```powershell
docker compose up --build
```

---

## Execute a shell command in API

```powershell
docker compose exec api <command>
```

---

## Run listener manually

The worker can also be executed as a one-off container:

```powershell
docker compose run --rm api python -m app.workers.listener
```

This creates a temporary container using the backend service configuration but overrides the normal FastAPI startup command.

---

## Open PostgreSQL CLI

```powershell
docker compose exec db psql -U meme_trade -d meme_trade
```

Exit with:

```text
\q
```

---

# Database Migrations

TerMEMEal uses Alembic for database schema management.

Alembic migration files track changes to the structure of the database.

They do **not** contain database records or serve as database backups.

---

## Create a migration

After modifying SQLAlchemy models:

```powershell
docker compose exec api python -m alembic revision --autogenerate -m "describe migration"
```

Example:

```powershell
docker compose exec api python -m alembic revision --autogenerate -m "create discoveries table"
```

Always inspect autogenerated migration files before applying them.

---

## Apply migrations

```powershell
docker compose exec api python -m alembic upgrade head
```

---

## Migration architecture

```text
SQLAlchemy Models
       ↓
Alembic compares metadata
       ↓
Migration file
       ↓
alembic upgrade head
       ↓
PostgreSQL schema updated
```

Migration files are committed to Git.

Database records are not.

---

# Frontend Data Flow

The current frontend uses REST polling.

```text
React mounts DiscoveryFeed
        ↓
TanStack Query
        ↓
GET /api/discoveries
        ↓
FastAPI
        ↓
PostgreSQL
        ↓
JSON response
        ↓
TanStack cache
        ↓
React render
```

Every few seconds:

```text
TanStack Query
      ↓
refetch
      ↓
new database state
      ↓
React update
```

---

# Discovery Status Updates

A token does not need to be recreated when its state changes.

For example:

Initial database state:

```text
id:            42
symbol:        MEME
exchange:      pumpfun
status:        watching
graduated_at:  NULL
```

After graduation:

```text
id:            42
symbol:        MEME
exchange:      pumpswap
status:        graduated
graduated_at:  2026-08-14...
```

The database ID remains:

```text
42
```

so React continues treating the object as the same logical card.

---

# Reliability and Recovery

Several reliability mechanisms already exist.

## WebSocket reconnect

The discovery listener automatically reconnects to DexScreener after connection failures.

---

## PostgreSQL persistence

Discovery information survives container restarts.

---

## Unique token addresses

Database uniqueness prevents duplicate token rows.

---

## Upsert behavior

Repeated discovery events can update an existing token rather than creating duplicates.

---

## Container restart policy

The discovery worker can be configured with:

```yaml
restart: unless-stopped
```

allowing Docker to restart the process after failures.

---

# Current Reliability Limitation

The Pump.fun graduation watch currently exists partly in process memory.

Conceptually:

```python
graduation_watch = {}
```

The token itself is persisted to PostgreSQL, but the in-memory watch list is lost if the listener process restarts.

Example:

```text
Pump.fun detected
      ↓
database row created
      ↓
graduation watch added
      ↓
listener restarts
      ↓
database row survives
      ↓
in-memory watch entry lost
```

A planned improvement is to reconstruct the watch list on startup from database rows matching:

```text
exchange = pumpfun
status = watching
```

This will make PostgreSQL the complete source of truth for discovery lifecycle recovery.

---

# Current Limitations

The following features are intentionally not complete yet.

## No live SSE stream

Frontend discovery updates currently use five-second polling.

---

## Trading backend not implemented

The UI contains trading controls, but they are not yet connected to real blockchain transactions.

---

## No wallet integration

Wallet connection status is currently UI-level functionality.

---

## No authentication

The current local development application does not implement users or access control.

---

## No multi-user state

Discovery state is currently global.

If user-specific discovery dismissal or preferences are added later, these will require separate user-state tables.

---

## No production deployment

Current infrastructure is optimized for local Docker development.

---

## No complete worker recovery

Graduation state is not yet reconstructed from PostgreSQL on listener startup.

---

# Planned Features

## Server-Sent Events

Replace or supplement polling with:

```text
GET /api/discoveries/stream
```

Expected architecture:

```text
listener
   ↓
database
   ↓
event notification
   ↓
FastAPI SSE
   ↓
browser EventSource
   ↓
TanStack Query cache
   ↓
React
```

This will allow near-instant discovery updates.

---

## Discovery dismissal

Cards will eventually support an `X` / dismiss operation.

Rather than deleting the discovery:

```text
dismissed_at = timestamp
```

will preserve historical data while removing it from the active feed.

---

## Listener state restoration

At startup:

```text
SELECT pumpfun discoveries
WHERE status = watching
```

will rebuild graduation monitoring.

---

## Trading Execution

Future trade flow:

```text
React
   ↓
FastAPI
   ↓
Trading Service
   ↓
Solana transaction
   ↓
transaction persistence
   ↓
React status update
```

Potential features include:

- buy token
- sell token
- amount selection
- slippage configuration
- timed sells
- transaction history
- trade status
- paper trading
- real trading safety controls

---

## Transaction Database

A future transaction model may store:

- transaction ID
- token address
- side
- quantity
- SOL amount
- execution price
- slippage
- blockchain signature
- timestamp
- status
- realized P/L

---

## Historical Discovery Data

Future views may provide:

- recent discoveries
- dismissed discoveries
- graduated tokens
- exchange filters
- discovery time filters
- token search

---

## Market Data

Future integrations may include:

- token price
- market capitalization
- liquidity
- volume
- transaction counts
- OHLCV candles
- token age
- return metrics

---

## Production Infrastructure

Potential AWS deployment architecture:

```text
React
 ↓
S3 / CloudFront

FastAPI
 ↓
ECS / Fargate

Discovery Worker
 ↓
ECS / Fargate

PostgreSQL
 ↓
Amazon RDS

Secrets
 ↓
AWS Secrets Manager

Logs
 ↓
CloudWatch
```

Kubernetes / EKS may be explored later once the application has enough independent services and operational complexity to justify it.

---

# Architecture Principles

## Keep HTTP separate from background processing

FastAPI handles requests.

The listener handles continuous external event processing.

```text
FastAPI != discovery loop
```

---

## Keep external providers separate from business logic

DexScreener communication should remain isolated from application rules where practical.

As the worker grows, it may eventually be split into:

```text
workers/
├── listener.py
└── dexscreener.py
```

with:

```text
dexscreener.py
```

handling provider-specific networking and:

```text
listener.py
```

handling application orchestration.

---

## Keep database operations in repositories

Application services should not need to know the exact SQL used to store data.

```text
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

---

## Keep API schemas separate from database models

SQLAlchemy models describe:

> how data is stored

Pydantic schemas describe:

> how data enters and leaves the API

These are deliberately separate concepts.

---

## PostgreSQL is the source of truth

Process-local Python state should only be used for temporary runtime bookkeeping.

Durable application state belongs in PostgreSQL.

---

## React does not own server state

React handles interface state.

TanStack Query handles remote server state.

This prevents components from manually implementing unnecessary cache and refresh logic.

---

## Containers should be replaceable

Application containers are treated as disposable processes.

Persistent data is stored outside them.

```text
container
   ↓
can disappear

PostgreSQL volume
   ↓
data remains
```

---

# Development Philosophy

TerMEMEal is being built incrementally.

Rather than implementing the entire trading system immediately, each layer is being validated independently.

The development progression has roughly been:

```text
React UI
   ↓
Dockerized frontend
   ↓
FastAPI
   ↓
REST API
   ↓
PostgreSQL
   ↓
SQLAlchemy
   ↓
Alembic
   ↓
live discovery worker
   ↓
database persistence
   ↓
live dashboard updates
   ↓
token lifecycle tracking
   ↓
real-time events
   ↓
trading services
   ↓
cloud deployment
```

This approach keeps individual architectural changes understandable and testable while gradually building toward a complete distributed application.

---

# Summary

TerMEMEal currently demonstrates a working full-stack asynchronous data pipeline:

```text
External WebSocket
        ↓
Python async worker
        ↓
Application service
        ↓
SQLAlchemy repository
        ↓
PostgreSQL
        ↓
FastAPI REST API
        ↓
TanStack Query
        ↓
React + TypeScript
```

The application already supports persistent real-world token discovery, lifecycle updates, independent backend processes, database migrations, container orchestration, and reactive frontend updates.

The next major phases will focus on improving real-time communication, strengthening worker recovery, implementing trading operations, recording transactions, and preparing the system for cloud deployment.