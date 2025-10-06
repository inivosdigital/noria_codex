# Infrastructure

This directory hosts database migration scripts, seed data, and environment configuration required for the Noria platform. Local development uses the Dockerized Postgres instance (`docker-compose.postgres.yml`), while production remains Supabase-compatible.

- `migrations/` – SQL migration files managed outside Alembic when needed.
- `seed/` – Seed data for local development and test fixtures.
- `supabase/` – Supabase deployment configuration (retained for hosted environments).
