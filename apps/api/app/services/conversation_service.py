"""Service managing conversations."""
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation import ConversationRepository


class ConversationService:
    """Wrapper around the conversation repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = ConversationRepository(session)

    async def create_message(self, user_id: UUID, message_text: str, sender_type: str):
        return await self._repo.create(user_id=user_id, message_text=message_text, sender_type=sender_type)

    async def list_messages(self, user_id: UUID) -> Sequence:
        return await self._repo.list_for_user(user_id)

    async def get_message(self, conversation_id: UUID):
        return await self._repo.get(conversation_id)

    async def update_message(
        self,
        conversation_id: UUID,
        *,
        message_text: str | None = None,
        sender_type: str | None = None,
    ):
        return await self._repo.update(conversation_id, message_text=message_text, sender_type=sender_type)

    async def delete_message(self, conversation_id: UUID) -> None:
        await self._repo.delete(conversation_id)


__all__ = ["ConversationService"]
