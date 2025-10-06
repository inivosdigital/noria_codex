# Development Workflow

## Third-Party Account Setup

Complete these steps before running Story 1.0 so credentials exist for later automation. Record generated keys in a password manager or secrets vault.

### 1. Supabase Project

1. Sign up or log in at https://app.supabase.com (free tier sufficient).
2. Create a new project named `noria` in the US East region.
3. Capture the Project URL and `anon`/`service_role` keys from Project Settings → API.
4. Enable the following features under Auth → Settings: email/password sign-in, password reset emails, and session length of 24 hours.
5. Configure custom SMTP provider (see Email Service section) or stick with Supabase-hosted emails for MVP.

### 2. Vercel

1. Sign up at https://vercel.com using GitHub SSO for seamless repo imports.
2. Create a new Vercel project pointing to the GitHub repository once it exists.
3. Set environment variables (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `ANTHROPIC_API_KEY`, etc.) for the project under Settings → Environment Variables.
4. Optional: configure preview protection (password-protected previews) for privacy.

### 3. Anthropic (Claude)

1. Request API access at https://console.anthropic.com/.
2. Once approved, create an API key in the dashboard.
3. Store the key securely; add it to Vercel + local `.env` files as `ANTHROPIC_API_KEY`.
4. Set initial spending limits and alerts in the console to stay within the MVP budget.

### 4. GitHub Secrets

1. In the GitHub repository, navigate to Settings → Secrets and variables → Actions.
2. Add secrets for each environment: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
3. Use GitHub Environments (`preview`, `staging`, `production`) to scope secrets per branch.

Record completion of these steps in the project log so future contributors can confirm prerequisites quickly.

## Local Development Setup

**Prerequisites**

- Node.js 20.x LTS (install via Volta, nvm, or asdf)
- pnpm 9.x (enable through Corepack)
- Python 3.11.x with `uv` package manager
- Docker Desktop or Podman (for the local Postgres container)
- Supabase CLI 1.150.0+ (optional for managed Supabase workflows)
- Git 2.44+

**Verify tooling**

```bash
node --version
npm --version
pnpm --version
python3 --version
uv --version
docker --version
```

### Day-0 bootstrap sequence

Use these steps to reproduce the initial scaffolding captured by Story 1.0. They create the Turborepo workspace structure and stub applications described in the architecture.

1. **Initialize repository root**
   ```bash
   mkdir noria && cd noria
   git init
   corepack enable
   pnpm init -y
   pnpm add -D turbo typescript eslint prettier
   ```
2. **Create monorepo workspace layout**
   ```bash
   mkdir -p apps/web apps/api packages/shared/src/{types,constants,utils} packages/config/{eslint,typescript,tailwind} infrastructure/{migrations,seed,supabase/functions} scripts docs
   touch turbo.json pnpm-workspace.yaml README.md
   ```
3. **Scaffold Next.js frontend**
   ```bash
   pnpm dlx create-next-app@latest apps/web --ts --tailwind --eslint --app --src-dir false --import-alias "@/*" --use-pnpm
   cd apps/web
   pnpm dlx shadcn-ui@latest init --yes
   pnpm dlx shadcn-ui@latest add button input textarea card dialog form toast
   cd ../..
   ```
   Remove demo routes/components and add the placeholder folders listed in `docs/NORIA_FULLSTACK_ARCHITECTURE/unified-project-structure.md`.

4. **Scaffold FastAPI service**
   ```bash
   uv init apps/api --python 3.11 --package fastapi --package "uvicorn[standard]" --package pydantic --package sqlalchemy --package python-dotenv
   ```
   Create `apps/api/app/main.py` with a stub FastAPI application and add empty package modules (`api`, `core`, `models`, `services`, `repositories`, `tasks`, `utils`).

5. **Prepare shared packages**
   ```bash
   (cd packages/shared && pnpm init -y && pnpm add typescript --save-dev)
   (cd packages/config && pnpm init -y)
   touch packages/shared/src/index.ts packages/config/eslint/index.cjs packages/config/typescript/base.json packages/config/tailwind/base.js
   ```

6. **Baseline configuration files**
   ```bash
   cp apps/web/.env.local.example ./.env.example
   cp apps/api/.env.example infrastructure/.env.example 2>/dev/null || true
   cat > turbo.json <<'EOF'
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": ["dist/**", ".next/**"]
       },
       "lint": {},
       "test": {
         "dependsOn": ["lint"]
       }
     }
   }
   EOF
   ```
   Populate workspace, lint, test, and formatting scripts inside the root `package.json` after this step.

7. **Commit initial scaffold**
   ```bash
   git add .
   git commit -m "chore: bootstrap Noria mono-repo"
   ```

### Standard workspace install

Once the repository exists, every developer performs the following to get productive locally.

```bash
corepack enable
pnpm install
uv sync --from apps/api
cp apps/web/.env.local.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env
docker compose -f docker-compose.postgres.yml up -d  # boots local Postgres
pnpm turbo run lint --parallel
pnpm turbo run test --parallel
```

Stop the database container with `docker compose -f docker-compose.postgres.yml down` when you finish developing. Use Supabase CLI only when targeting hosted environments.

### Launching development servers

Run application processes in parallel once dependencies and local services are ready.

```bash
pnpm --filter web dev               # Next.js frontend at http://localhost:3000
uv run --cwd apps/api uvicorn app.main:app --reload --port 8000  # FastAPI backend
```

Use Turborepo when you want a single command to coordinate both apps:

```bash
pnpm turbo run dev --parallel --filter=web --filter=api
```

## Database Change Management

### Migration workflow

1. Ensure the Docker Postgres container is running (`docker compose -f docker-compose.postgres.yml up -d`).
2. Activate the backend environment: `uv sync --from apps/api && uv run --cwd apps/api alembic upgrade head`.
3. To create a new migration, run:
   ```bash
   uv run --cwd apps/api alembic revision --autogenerate -m "describe change"
   ```
4. Apply pending migrations locally with:
   ```bash
   uv run --cwd apps/api alembic upgrade head
   ```
5. For Supabase remote environments, use the managed migrations folder under `infrastructure/migrations/` and deploy with:
   ```bash
   supabase db push --env prod
   ```
6. Commit both the Alembic version file and any Supabase SQL migration files together to keep state consistent.

### Seed data workflow

1. Add SQL seed scripts inside `infrastructure/seed/` (e.g., `development.sql`, `crisis_resources.sql`).
2. Provide Python-based fixtures inside `apps/api/scripts/seed_data.py` for complex initialization.
3. Execute database seeds during local setup with:
   ```bash
   docker compose -f docker-compose.postgres.yml exec postgres \
     psql -U postgres -d postgres -f infrastructure/seed/development.sql
   uv run --cwd apps/api python scripts/seed_data.py
   ```
4. Document any mandatory seed steps in story acceptance criteria when new tables are introduced. For hosted environments, mirror seeds via Supabase CLI (`supabase db reset --seed ...`).

All migrations and seed scripts should be referenced in release notes so deployment timelines can account for data changes.

## Environment Configuration

1. **Root env file (`.env.example`)** – holds shared secrets (local Postgres credentials by default, Supabase keys when deploying). Duplicate to `.env` for local overrides.
2. **Frontend (`apps/web/.env.local.example`)** – browser-safe settings only (Next.js convention). Copy to `.env.local` before running the dev server.
3. **Backend (`apps/api/.env.example`)** – FastAPI configuration. Copy to `.env` and keep secrets out of version control.
4. **Infrastructure (`infrastructure/.env.example`)** – parameters for seed scripts and Supabase migrations. Copy into `.env` before running migration scripts.

Refresh `.env` files whenever credentials rotate. Use the architecture repo’s `coding-standards.md` guidance for schema-validating environment variables before accessing them in code.

## Database Migration & Seed Workflow

1. Make schema or SQLAlchemy model changes inside `apps/api`.
2. Generate migration script:
   ```bash
   uv run --cwd apps/api alembic revision --autogenerate -m "describe change"
   ```
3. Review and edit the generated file; ensure new constraints, indexes, and RLS
   policies are included. Add complementary seed data updates if required.
4. Apply locally:
   ```bash
   docker compose -f docker-compose.postgres.yml down --volumes
   docker compose -f docker-compose.postgres.yml up -d
   uv run --cwd apps/api alembic upgrade head
   docker compose -f docker-compose.postgres.yml exec postgres \
     psql -U postgres -d postgres -f infrastructure/seed/base_seed.sql
   ```
5. Run backend + integration tests before committing:
   ```bash
   uv run --cwd apps/api pytest
   pnpm turbo run test --filter api
   pnpm --filter web test:e2e -- --headed=false
   ```
6. Commit migration and updated docs. CI will replay the above commands in the
   `ci.yml` workflow and block merges on failure.

Preview environments automatically execute migrations and apply seed fixtures
using `infrastructure/seed/test_seed.sql`. Staging refreshes nightly from
production snapshots with personal data anonymized.

## Testing & Tooling Reference

| Scope | Command | Notes |
|-------|---------|-------|
| Linting | `pnpm turbo run lint` | ESLint (frontend) + Ruff (backend via pre-commit) |
| Frontend unit | `pnpm --filter web test` | Jest + React Testing Library |
| Shared packages | `pnpm --filter shared test` | Vitest |
| Backend unit/integration | `uv run --cwd apps/api pytest` | httpx TestClient + database fixtures |
| Contract tests | `pnpm turbo run test --filter contracts` | Pact with provider/consumer assertions |
| E2E smoke | `pnpm --filter web test:e2e -- --headed=false` | Playwright against local stack |
| Accessibility | `pnpm --filter web test:a11y` | Axe CLI in CI nightly |

Git hooks (configured via Husky) run lint + unit tests pre-push. CI executes the
same suite plus coverage checks; failures must be resolved before deployment.

## CI/CD Touchpoints

- GitHub Actions publish Vercel preview URLs on every PR and validate Supabase migrations using the CLI.
- Merges to `main` trigger the release workflow that applies Alembic/Supabase migrations, deploys Vercel (frontend + API), and performs `/health` smoke checks.
- Rollbacks use `vercel rollback <deployment-id>`; if schema changes are involved, run the matching Alembic downgrade and `supabase db reset --project-ref ...` to align remote state.
