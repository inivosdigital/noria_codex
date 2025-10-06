# Backend Architecture

## Service Architecture

The FastAPI application follows a layered architecture that mirrors the repository structure defined in `docs/NORIA_FULLSTACK_ARCHITECTURE/unified-project-structure.md`. Each layer has a single responsibility and exposes clear interfaces so that future services or background workers can reuse the same components.

```text
apps/api/app/
├── api/                # Route definitions and request/response schemas
│   └── v1/             # Versioned API namespaces
│       ├── auth/       # Authentication and session management endpoints
│       ├── chat/       # Coaching conversation endpoints
│       ├── crisis/     # Crisis detection + resources endpoints
│       ├── wellness/   # Resource library management
│       └── __init__.py
├── core/               # Application configuration and cross-cutting concerns
│   ├── config.py       # Pydantic settings + environment loading
│   ├── database.py     # SQLAlchemy engine/session + Supabase connection helpers
│   ├── security.py     # Password hashing, token utilities, RLS helpers
│   └── logging.py      # Structured logging configuration
├── models/             # Pydantic domain models used across layers
├── repositories/       # Data access layer that wraps SQLAlchemy queries
├── services/           # Business logic orchestrating repositories + external APIs
├── tasks/              # Background job definitions (pg-boss / Celery workers)
├── utils/              # Shared helpers (validators, exceptions, formatting)
└── main.py             # FastAPI application factory
```

Each route module (`api/v1/.../routes.py`) depends on the corresponding service through dependency injection. Services may collaborate with repositories and other services, but never reach directly into request objects. Repositories return domain objects (Pydantic models) rather than raw SQL rows to keep the service layer testable.

## Application Factory

`main.py` exposes a `create_app()` function that wires the FastAPI instance, registers middleware, and mounts routers. The factory pattern enables distinct configurations for local development, testing, and production. Example responsibilities:

- load settings by calling `core.config.get_settings()`
- configure logging according to environment
- initialize database session dependency (`core.database.get_session`)
- register middleware (CORS, correlation IDs, rate limiting)
- include API routers and attach tags/metadata
- mount `/health` and `/metrics` endpoints

The Uvicorn entry in development should import `create_app()` to avoid module-level side effects.

## Dependency Injection

FastAPI dependencies live in `api/dependencies.py` modules. Key providers:

- `get_settings()` – returns cached Pydantic settings object
- `get_db()` – yields a SQLAlchemy session scoped to the request
- `require_authenticated_user()` – validates Supabase JWT, attaches `user_id` to request state
- `get_chat_service()` / `get_crisis_service()` – instantiate services with repositories and external clients

Dependencies should be composed at the router level so unit tests can override them easily.

## Middleware & Cross-cutting Concerns

Mandatory middleware stack:

1. **Request ID middleware** – injects `X-Request-ID` header and stores correlation ID in contextvars for structured logging.
2. **CORS middleware** – allow-listed origins based on environment settings.
3. **Authentication guard** – FastAPI dependency that validates Supabase access tokens and populates `request.state.user`.
4. **Rate limiting** – Optional for MVP, but scaffolded using `slowapi` to protect crisis endpoints.
5. **Error normalization** – Catch `HTTPException` and custom `DomainError` types, translate to the unified JSON error format defined in `docs/NORIA_FULLSTACK_ARCHITECTURE/error-handling-strategy.md`.

## Background Processing

Long-running work (ChAT scoring, crisis follow-up notifications) is offloaded to pg-boss queues managed by Supabase. The `tasks/` package exposes functions that can be triggered either by database triggers (see `database-schema.md` queue trigger) or by scheduled jobs. Each task receives lightweight input payloads and calls the same service layer used by HTTP routes to avoid business logic drift.

Background workers run via:

```bash
uv run --cwd apps/api python tasks/worker.py
```

Workers reuse the settings module so they can connect to Supabase/Postgres with the same credentials as the web app.

## External Integrations

External clients (Anthropic Claude, wellness resource feeds, email providers) live under `services/integrations/`. Each client exposes a thin interface with retry/circuit-breaker behavior. The chat service composes these clients so that API routes can remain oblivious to vendor details.

When adding a new integration:

1. Define an interface protocol (e.g., `ClaudeClient`) in `services/interfaces.py`.
2. Implement the client with resilience features (timeouts, retries, fallback responses).
3. Register the client in dependency wiring so tests can substitute fakes.
4. Update `core.config` with any required environment variables and default values.

## Observability

- Structure all logs as JSON via `core.logging.configure_logging()`. Include correlation IDs, user IDs (when available), and request path/status.
- Export Prometheus metrics via `prometheus-fastapi-instrumentator` mounted at `/metrics`.
- Surface critical business events (crisis detected, graduation achieved) via structured logs plus optional webhook notifications for operations staff.

## Testing Strategy Alignment

- Repository unit tests may mock the database session using an in-memory SQLite engine configured to mimic PostgreSQL constraints where possible.
- Service unit tests can patch integration clients to deterministic fakes; integration tests must exercise the real adapters against the local Supabase + worker stack.
- API contract tests run with the real DI stack and a transactional test database seeded by fixtures.
- Background task tests simulate queue payloads through the actual pg-boss worker pipeline to assert idempotent behavior.

Documenting these expectations keeps the backend ready for automation by developer agents while preserving clarity for future refactors.
