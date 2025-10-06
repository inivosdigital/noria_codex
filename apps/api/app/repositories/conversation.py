"""Conversation repository."""
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select

from app.models.conversation import Conversation
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository):
    """Data access for conversations."""

    async def create(
        self,
        user_id: UUID,
        message_text: str,
        sender_type: str,
    ) -> Conversation:
        record = Conversation(user_id=user_id, message_text=message_text, sender_type=sender_type)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def list_for_user(self, user_id: UUID) -> Sequence[Conversation]:
        result = await self.session.execute(
            select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.timestamp)
        )
        return result.scalars().all()

    async def get(self, conversation_id: UUID) -> Optional[Conversation]:
        result = await self.session.execute(select(Conversation).where(Conversation.id == conversation_id))
        return result.scalar_one_or_none()

    async def update(
        self,
        conversation_id: UUID,
        *,
        message_text: str | None = None,
        sender_type: str | None = None,
    ) -> Optional[Conversation]:
        record = await self.get(conversation_id)
        if record is None:
            return None

        if message_text is not None:
            record.message_text = message_text
        if sender_type is not None:
            record.sender_type = sender_type

        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def delete(self, conversation_id: UUID) -> None:
        record = await self.get(conversation_id)
        if record is None:
            return
        await self.session.delete(record)
        await self.session.commit()


__all__ = ["ConversationRepository"]
