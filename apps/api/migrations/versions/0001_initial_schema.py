"""Initial schema for users, conversations, and analysis results.

This migration follows the database specification documented in
`docs/NORIA_FULLSTACK_ARCHITECTURE/database-schema.md` and now enables the
Supabase-style Row Level Security (RLS) policies plus the analysis queue
trigger referenced by the architecture docs.
"""
from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("goals", sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column("stage", sa.Integer(), nullable=False, server_default="1"),
    )

    op.create_table(
        "conversations",
        sa.Column(
            "id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("sender_type", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.CheckConstraint(
            "sender_type IN ('user', 'coach', 'system')",
            name="conversations_sender_type_chk",
        ),
    )

    op.create_table(
        "analysis_results",
        sa.Column(
            "id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chat_score", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("message_range", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "job_queue",
        sa.Column(
            "id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "data",
            sa.dialects.postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("retry_limit", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "start_after",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index("ix_conversations_user_id", "conversations", ["user_id"])
    op.create_index("ix_analysis_results_user_id", "analysis_results", ["user_id"])

    # Ensure auth.uid() exists so policy creation succeeds even outside Supabase.
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_proc p
                JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'auth' AND p.proname = 'uid'
            ) THEN
                EXECUTE 'CREATE SCHEMA IF NOT EXISTS auth';
                EXECUTE $$CREATE OR REPLACE FUNCTION auth.uid() RETURNS uuid
                    LANGUAGE sql STABLE
                AS $$ SELECT NULL::uuid $$;$$;
            END IF;
        END;
        $$;
        """
    )

    op.execute("ALTER TABLE IF EXISTS public.users ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE IF EXISTS public.conversations ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE IF EXISTS public.analysis_results ENABLE ROW LEVEL SECURITY")

    op.execute(
        """
        CREATE POLICY "Users can view their own data" ON public.users
            FOR SELECT
            USING (auth.uid() = id);
        """
    )
    op.execute(
        """
        CREATE POLICY "Users can update their own data" ON public.users
            FOR UPDATE
            USING (auth.uid() = id);
        """
    )
    op.execute(
        """
        CREATE POLICY "Users can view their own conversations" ON public.conversations
            FOR SELECT
            USING (auth.uid() = user_id);
        """
    )
    op.execute(
        """
        CREATE POLICY "Users can insert their own messages" ON public.conversations
            FOR INSERT
            WITH CHECK (auth.uid() = user_id);
        """
    )
    op.execute(
        """
        CREATE POLICY "Users can view their own analysis" ON public.analysis_results
            FOR SELECT
            USING (auth.uid() = user_id);
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION public.queue_analysis_check()
        RETURNS TRIGGER AS $$
        DECLARE
            user_message_count integer;
        BEGIN
            SELECT COUNT(*)
              INTO user_message_count
              FROM public.conversations
             WHERE user_id = NEW.user_id AND sender_type = 'user';

            IF user_message_count > 0 AND user_message_count % 25 = 0 THEN
                INSERT INTO public.job_queue (name, data)
                VALUES ('analysis_job', jsonb_build_object('user_id', NEW.user_id));
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trigger_analysis_queue
        AFTER INSERT ON public.conversations
        FOR EACH ROW EXECUTE FUNCTION public.queue_analysis_check();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trigger_analysis_queue ON public.conversations")
    op.execute("DROP FUNCTION IF EXISTS public.queue_analysis_check")

    op.execute(
        """
        DROP POLICY IF EXISTS "Users can view their own analysis" ON public.analysis_results;
        DROP POLICY IF EXISTS "Users can insert their own messages" ON public.conversations;
        DROP POLICY IF EXISTS "Users can view their own conversations" ON public.conversations;
        DROP POLICY IF EXISTS "Users can update their own data" ON public.users;
        DROP POLICY IF EXISTS "Users can view their own data" ON public.users;
        """
    )

    op.execute("ALTER TABLE IF EXISTS public.analysis_results DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE IF EXISTS public.conversations DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE IF EXISTS public.users DISABLE ROW LEVEL SECURITY")

    op.drop_index("ix_analysis_results_user_id", table_name="analysis_results")
    op.drop_index("ix_conversations_user_id", table_name="conversations")

    op.drop_table("job_queue")
    op.drop_table("analysis_results")
    op.drop_table("conversations")
    op.drop_table("users")
