"""Shared pytest fixtures for the API package."""
import asyncio
import os
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models import Base


def _load_env_file() -> None:
    """Populate os.environ with values from the project .env file if not already set."""

    env_path = Path(__file__).resolve().parents[1] / ".env"
    # Fall back to workspace-level .env if the apps/api scoped file is missing
    if not env_path.exists():
        env_path = Path(__file__).resolve().parents[3] / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if sep != "=":
            continue
        os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def _get_database_url() -> str:
    _load_env_file()
    database_url = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    return os.path.expandvars(database_url)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _database_url() -> str:
    return _get_database_url()


@pytest.fixture(scope="session")
async def _engine(_database_url: str) -> AsyncIterator[tuple[AsyncEngine, str]]:
    engine = create_async_engine(
        _database_url,
        future=True,
        poolclass=NullPool,
        execution_options={"isolation_level": "AUTOCOMMIT"},
        connect_args={"ssl": False},
    )
    backend = make_url(_database_url).get_backend_name()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine, backend
    finally:
        if backend.startswith("sqlite"):
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.fixture()
async def db_session(_engine: tuple[AsyncEngine, str]) -> AsyncIterator[AsyncSession]:
    engine, backend = _engine
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
