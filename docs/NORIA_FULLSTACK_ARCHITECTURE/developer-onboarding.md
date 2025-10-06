# Developer Onboarding Checklist

1. **Access & Accounts**
   - GitHub repo access granted
   - Supabase project access (dashboard + CLI)
   - Vercel project access
   - Anthropic API key provided via 1Password/secret vault

2. **Local Environment Setup**
   - Review `development-workflow.md`
   - Install Node.js 20, pnpm, Python 3.11, uv, Docker
   - Run Day-0 bootstrap (or `pnpm install`, `uv sync`, `supabase start` for existing repo)

3. **Read Required Docs**
   - `development-workflow.md`
   - `frontend-architecture.md`
   - `backend-architecture.md`
   - `security-and-performance.md`
   - `coding-standards.md`

4. **Run Baseline Tests**
   - `pnpm turbo run lint`
   - `pnpm turbo run test`
   - `uv run --cwd apps/api pytest`
   - `pnpm --filter web test:e2e`

5. **Credentials & Env Files**
   - Copy `.env.example` → `.env`
   - Fill in Supabase, Anthropic keys, etc.

6. **Working with Stories**
   - Read assigned story file under `docs/stories`
   - Follow develop-story procedure (tasks, tests, file list updates)

7. **Code Review Expectations**
   - Write clear PR descriptions referencing story
   - Include test results
   - Tag reviewers (peer + tech lead)

8. **Incident & Rollback Awareness**
   - Review uptime playbook (health checks, `vercel rollback`, Supabase PITR)
   - Know incident response contacts

9. **Security & Privacy**
   - Use validated environment access (no raw `process.env`)
   - Respect RLS policies; don’t bypass with service role
   - Follow encryption & privacy guidance when working with conversation data

10. **First PR**
    - Pair with senior dev for initial merge
    - Confirm CI (lint/test/e2e) passes before requesting review
