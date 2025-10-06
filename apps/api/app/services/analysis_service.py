"""Service managing analysis results."""
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analysis import AnalysisRepository


class AnalysisService:
    """Business logic for analysis records."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = AnalysisRepository(session)

    async def create_result(self, user_id: UUID, chat_score: int, message_range: str | None = None):
        return await self._repo.create(user_id=user_id, chat_score=chat_score, message_range=message_range)

    async def list_results(self, user_id: UUID) -> Sequence:
        return await self._repo.list_for_user(user_id)

    async def get_result(self, analysis_id: UUID):
        return await self._repo.get(analysis_id)

    async def update_result(
        self,
        analysis_id: UUID,
        *,
        chat_score: int | None = None,
        message_range: str | None = None,
    ):
        return await self._repo.update(analysis_id, chat_score=chat_score, message_range=message_range)

    async def delete_result(self, analysis_id: UUID) -> None:
        await self._repo.delete(analysis_id)


__all__ = ["AnalysisService"]
