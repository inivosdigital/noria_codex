"""Analysis repository."""
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select

from app.models.analysis import AnalysisResult
from app.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository):
    """CRUD operations for analysis results."""

    async def create(
        self,
        user_id: UUID,
        chat_score: int,
        message_range: str | None = None,
    ) -> AnalysisResult:
        record = AnalysisResult(user_id=user_id, chat_score=chat_score, message_range=message_range)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def list_for_user(self, user_id: UUID) -> Sequence[AnalysisResult]:
        result = await self.session.execute(
            select(AnalysisResult).where(AnalysisResult.user_id == user_id).order_by(AnalysisResult.timestamp)
        )
        return result.scalars().all()

    async def get(self, analysis_id: UUID) -> Optional[AnalysisResult]:
        result = await self.session.execute(select(AnalysisResult).where(AnalysisResult.id == analysis_id))
        return result.scalar_one_or_none()

    async def update(
        self,
        analysis_id: UUID,
        *,
        chat_score: int | None = None,
        message_range: str | None = None,
    ) -> Optional[AnalysisResult]:
        record = await self.get(analysis_id)
        if record is None:
            return None

        if chat_score is not None:
            record.chat_score = chat_score
        if message_range is not None:
            record.message_range = message_range

        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def delete(self, analysis_id: UUID) -> None:
        record = await self.get(analysis_id)
        if record is None:
            return
        await self.session.delete(record)
        await self.session.commit()


__all__ = ["AnalysisRepository"]
