# Deployment Architecture

## Deployment Strategy

| Surface      | Platform | Trigger                        | Notes |
|--------------|----------|--------------------------------|-------|
| Frontend PWA | Vercel   | Git push to any branch         | Preview URLs on PRs |
| API (FastAPI)| Vercel Serverless Functions | Built alongside frontend | Shares repo, uses edge runtime for lightweight endpoints |
| Background jobs | Supabase pg-boss workers (Edge Functions/Cron) | Triggered via migrations + scheduled cron | Processes analysis queues without dedicated servers |
| Database     | Supabase | Managed migrations via CLI     | Separate staging/production projects |

Promote code via the `develop → staging → main` branch strategy:

1. Feature branches deploy automatic Vercel previews and run full CI.
2. Merge into `develop` to trigger staging deployment (Vercel + Supabase staging).
3. After verification, merge `develop` into `main` to launch production deployments and run smoke tests.

## CI/CD Pipeline

GitHub Actions orchestrate builds and deployments using the workflow below (`.github/workflows/ci.yml`):

```yaml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: corepack enable
      - run: pnpm install
      - uses: astral-sh/setup-uv@v2
        with:
          version: '0.4.x'
      - run: uv sync --from apps/api
      - uses: supabase/setup-cli@v1
        with:
          version: '1.150.0'

  lint-test:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: ~/.pnpm-store
          key: ${{ runner.os }}-pnpm-${{ hashFiles('pnpm-lock.yaml') }}
      - run: corepack enable
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run lint
      - run: pnpm turbo run test --parallel
      - run: uv sync --from apps/api
      - run: uv run --cwd apps/api pytest

  e2e:
    needs: lint-test
    runs-on: ubuntu-latest
    services:
      supabase:
        image: supabase/postgres:15.1.0
        ports: [54321:5432]
    steps:
      - uses: actions/checkout@v4
      - run: corepack enable
      - run: pnpm install --frozen-lockfile
      - run: pnpm --filter web test:e2e

  deploy-preview:
    if: github.event_name == 'pull_request'
    needs: e2e
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./apps/web

  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: e2e
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: supabase db push --project-ref ${{ secrets.SUPABASE_PROD_REF }}
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./apps/web
          vercel-args: '--prod'
      - run: pnpm turbo run postdeploy
```

## Cloud Resource Provisioning

Follow this order whenever standing up a new environment to keep dependencies aligned:

1. **Supabase project**
   - Create the project (free tier) and record URL/keys.
   - Under Database → Backups, enable daily backups (included in free tier) to simplify rollback.
   - Configure Auth settings (email/password, password reset, session length) per technical assumptions.
   - Provision storage buckets (`assets` for static files) if needed by future stories.
   - Create SQL migrations for RLS policies and triggers via `supabase db diff` so infrastructure stays versioned.

2. **Vercel project**
   - Import the GitHub repository and link to Supabase project URL via environment variables.
   - Define build & dev commands (`pnpm turbo run build`, `pnpm turbo run dev`).
   - Configure preview/staging/production environment variables to match GitHub Secrets.
   - Enable Vercel Analytics and cron jobs (if used) from the dashboard.

3. **DNS / Domain (optional for MVP)**
   - For the free tier, Vercel provides a `*.vercel.app` domain. Custom domain purchase can be deferred until post-MVP.
   - If/when a custom domain is desired, add it in Vercel → Domains and follow the provided DNS records (CNAME/A). No acquisition is required at MVP stage to remain cost-free.

4. **Monitoring hooks**
   - Set up Supabase Log Drains (optional) and Vercel alerts. Capture webhook URLs in `infrastructure/monitoring/README.md`.

Document each provisioned resource in release notes; this provides an auditable sequence for future environments.

## Email & Messaging Service

To keep the MVP in the free tier, use Supabase's built-in email service for password reset and verification emails. Steps:

1. In Supabase Auth → Providers → Email, ensure SMTP settings are left blank so Supabase's default sender is used.
2. Customize email templates (Auth → Templates) with Noria branding and support contact info.
3. Monitor usage under Auth → Activity; Supabase free tier covers low-volume transactional emails used by the MVP.
4. If delivery becomes unreliable, switch to a free plan on providers like Resend or Mailgun and update SMTP credentials in Supabase settings.

Real-time messaging relies on Supabase Realtime (included for free). No additional messaging provider is required for the MVP scope.

## Infrastructure as Code

- **Supabase:** schema captured through Alembic migrations plus SQL files under `infrastructure/migrations/`. Use `supabase db pull` to sync managed schema changes.
- **Vercel:** environment configuration stored in `vercel.json` and the Vercel dashboard. Secrets mirrored in GitHub Actions using encrypted repository secrets.
- **Supabase background jobs:** queue definitions stored in `infrastructure/migrations/` and scheduled tasks documented in `infrastructure/jobs/README.md`.
- **Monitoring & alerts:** Vercel Analytics + Supabase logs configured via their respective dashboards; capture configuration exports in `infrastructure/monitoring/README.md`.

## Environment Matrix

| Environment | Branch | Services | Secrets Source | Notes |
|-------------|--------|----------|----------------|-------|
| Local       | any    | Docker Postgres, pnpm dev servers | `.env` | Full stack runs in Docker |
| Preview     | PR     | Vercel preview, temp Supabase DB | GitHub PR secrets | Auto-destroy when PR closes |
| Staging     | develop| Vercel staging, Supabase staging | GitHub environment secrets | Daily smoke tests + product reviews |
| Production  | main   | Vercel prod, Supabase prod | GitHub environment secrets | Requires manual approval step |

## Deployment Runbook

1. Confirm migrations in `apps/api/migrations` and `infrastructure/migrations` are committed.
2. Merge feature branch into `develop`; verify staging deploy + smoke tests (`pnpm turbo run smoke`).
3. Update release notes with migration summaries and seed requirements.
4. Merge `develop` into `main`; GitHub Actions will:
   - push Supabase migrations,
   - deploy Vercel frontend/API,
   - run post-deploy smoke script hitting `/health`, `/api/v1/status`, and crisis detection sample.
5. Monitor Vercel + Supabase dashboards for errors during first 30 minutes.
6. Rollback instructions:
   - `vercel rollback <deployment-id>`
   - `supabase db reset --project-ref ...` followed by `alembic downgrade -1` if schema regression required.

Document any manual infra adjustments (e.g., webhook endpoints, third-party API keys) in the release notes so future automation can catch up.
