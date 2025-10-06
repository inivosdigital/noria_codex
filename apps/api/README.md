# Noria API

This FastAPI application provides backend services for Noria. It uses async SQLAlchemy with a local Docker-hosted PostgreSQL database by default (Supabase-ready for deployment) and organises logic into repositories and services for clear separation of concerns.

## Quick Start

```bash
# from the repo root
docker compose -f docker-compose.postgres.yml up -d

# install Python deps (once)
uv sync

# launch the API (apps/api/.env already targets the local Postgres container)
uv run fastapi dev app/main.py
```

## Testing

```bash
uv run pytest
```

## Environment Configuration

The repo ships with a checked-in `.env.example`. Copy it to `.env` for local work:

```bash
cp apps/api/.env.example apps/api/.env
```

Populate the placeholders with freshly rotated Supabase credentials. The previous service role key has been scrubbed from version control; do not reuse it. Store the real secret outside Git (for example Vercel/Supabase project settings or local shell exports).

The development defaults use the Docker Postgres instance defined in `docker-compose.postgres.yml`.

## Security Hardening

- `/api/v1/auth/signup` is rate limited to 10 requests per minute per client IP by default. Override the limit via `AUTH_SIGNUP_RATE_LIMIT` and `AUTH_SIGNUP_RATE_WINDOW_SECONDS`.
- Password policy enforcement rejects weak credentials both at the service and API layers; integration tests cover negative paths.

