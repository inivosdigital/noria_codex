"""Base repository providing common helpers."""
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Base repository storing the session reference."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


__all__ = ["BaseRepository"]
