# Database Schema

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT NOT NULL,
    goals TEXT[] NOT NULL DEFAULT '{}',
    stage INTEGER NOT NULL DEFAULT 1 CHECK (stage IN (1, 2, 3)),
    profile JSONB NOT NULL DEFAULT '{}',
    preferences JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    graduation_date TIMESTAMP WITH TIME ZONE
);

-- Conversations table
CREATE TABLE public.conversations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    sender_type TEXT NOT NULL CHECK (sender_type IN ('user', 'assistant')),
    message_metadata JSONB NOT NULL DEFAULT '{}',
    analysis_included BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analysis results table
CREATE TABLE public.analysis_results (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    chat_score DECIMAL(3,1) NOT NULL CHECK (chat_score >= 0 AND chat_score <= 14),
    analysis_type TEXT NOT NULL CHECK (analysis_type IN ('chat_scoring', 'milestone_check', 'graduation_assessment', 'crisis_review')),
    message_range JSONB NOT NULL,
    insights JSONB NOT NULL DEFAULT '{}',
    improvement_areas TEXT[] NOT NULL DEFAULT '{}',
    strengths_identified TEXT[] NOT NULL DEFAULT '{}',
    triggered_milestone BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crisis events table
CREATE TABLE public.crisis_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    message_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    trigger_type TEXT NOT NULL,
    severity_level TEXT NOT NULL CHECK (severity_level IN ('low', 'moderate', 'high', 'critical')),
    keywords_detected TEXT[] NOT NULL DEFAULT '{}',
    resources_shown JSONB NOT NULL DEFAULT '[]',
    user_acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
    followup_required BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolution_timestamp TIMESTAMP WITH TIME ZONE
);

-- Job queue table (for pg-boss)
CREATE TABLE public.job_queue (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    data JSONB NOT NULL DEFAULT '{}',
    priority INTEGER NOT NULL DEFAULT 0,
    retry_limit INTEGER NOT NULL DEFAULT 3,
    retry_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    start_after TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_conversations_user_id_created_at ON public.conversations (user_id, created_at DESC);
CREATE INDEX idx_analysis_results_user_id_created_at ON public.analysis_results (user_id, created_at DESC);
CREATE INDEX idx_crisis_events_user_id_severity ON public.crisis_events (user_id, severity_level);
CREATE INDEX idx_job_queue_name_priority ON public.job_queue (name, priority DESC, created_at);

-- Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analysis_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crisis_events ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view their own data" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own data" ON public.users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can view their own conversations" ON public.conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own messages" ON public.conversations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can view their own analysis" ON public.analysis_results FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view their own crisis events" ON public.crisis_events FOR SELECT USING (auth.uid() = user_id);

-- Database functions and triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger for analysis queue
CREATE OR REPLACE FUNCTION queue_analysis_check()
RETURNS TRIGGER AS $$
BEGIN
    -- Queue analysis every 25 messages
    IF (SELECT COUNT(*) FROM public.conversations 
        WHERE user_id = NEW.user_id 
        AND sender_type = 'user' 
        AND analysis_included = FALSE) >= 25 THEN
        
        INSERT INTO public.job_queue (name, data)
        VALUES ('analysis_job', json_build_object('user_id', NEW.user_id));
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_analysis_queue AFTER INSERT ON public.conversations
    FOR EACH ROW EXECUTE FUNCTION queue_analysis_check();
```

## Migration Strategy

- **Tooling:** Alembic (managed through `uv` virtual env) generates migration
  scripts in `infrastructure/migrations`. Local runs execute against the Docker
  Postgres container, while Supabase CLI remains available for hosted targets.
- **Change Workflow:**
  1. Update SQLAlchemy models or raw SQL definitions.
  2. Create migration: `uv run --cwd apps/api alembic revision --autogenerate -m "<change>"`.
  3. Review the migration for accuracy (constraints, indexes, RLS policies).
  4. Apply locally: `uv run --cwd apps/api alembic upgrade head`.
  5. Run database tests (`pytest tests/db`) and Playwright smoke tests to catch
     regressions.
  6. Commit migration file alongside schema and doc updates.
- **Promotion:** CI runs migrations in staging via `supabase db push` (dry-run) +
  Alembic upgrade when deploying to Supabase. Production upgrades gate on staging
  success and require DBA approval. Rollback uses Alembic downgrade scripts stored
  in the same folder.

## Seed Data Plan

Seed data ensures developers and automated tests share deterministic fixtures.

- **Location:** `infrastructure/seed/`
  - `base_seed.sql` – minimal reference users, goals, conversation examples.
  - `test_seed.sql` – richer dataset for end-to-end tests (crisis scenarios,
    milestones, analysis snapshots).
  - `seed.py` – FastAPI script using repositories to insert records idempotently.
- **Execution:**
  - Local bootstrap: `docker compose -f docker-compose.postgres.yml exec postgres psql -U postgres -d postgres -f infrastructure/seed/base_seed.sql` followed by any Python seed scripts.
  - Test runs: CI loads `test_seed.sql` into the Docker container before running
    integration + Playwright suites (Supabase CLI may be used for hosted pipelines).
  - Staging: nightly job refreshes staging with anonymized production snapshot
    plus base seed overlay.
- **Data Hygiene:** Seeds avoid PII; crisis phrases come from synthetic lists.
  Migration scripts include data migrations when schema changes require
  backfilling.

Keep migration and seed artifacts synchronized with this document. Any schema
modification should update the SQL examples above and append instructions here.
