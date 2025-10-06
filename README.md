# Noria Monorepo

This repository hosts the Noria wellness platform as a monorepo. It contains a FastAPI backend and Next.js frontend, along with shared TypeScript types and infrastructure assets.

## Structure

- `apps/api` – FastAPI application with async PostgreSQL access via SQLAlchemy and Alembic migrations.
- `apps/web` – Next.js 15 app router project using React Hook Form and Zod for the signup experience.
- `packages/shared` – Shared TypeScript contracts consumed by the frontend.
- `infrastructure` – Database migrations, seed data, and environment configuration (Docker Postgres locally, Supabase for hosted deployments).

## Getting Started

1. Install JavaScript dependencies with `pnpm install`.
2. Sync Python dependencies with `uv sync` from `apps/api`.
3. Boot a local Postgres instance:
   ```bash
   docker compose -f docker-compose.postgres.yml up -d
   ```
4. Configure environment files:
   - Backend: copy `apps/api/.env` template (already using local Postgres) if you need to tweak secrets.
5. Run services:
   - Backend: `pnpm dev:api`
   - Frontend: `pnpm dev`

## Testing

- Backend: `uv run pytest`
- Frontend: `pnpm --filter noria-web test`
