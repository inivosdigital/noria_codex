"""Database engine and session management."""
from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import get_settings


_settings = get_settings()
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Return a singleton async engine instance."""

    global _engine
    if _engine is None:
        _engine = create_async_engine(
            _settings.database_url,
            pool_pre_ping=True,
            echo=_settings.environment == "local",
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Create the async session factory if needed."""

    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that yields a database session."""

    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def verify_database_connection() -> None:
    """Run a lightweight query to confirm credentials work."""

    async with get_session_factory()() as session:
        await session.execute(text("SELECT 1"))


__all__ = ["get_db_session", "get_engine", "verify_database_connection"]
