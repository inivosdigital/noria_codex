"""Conversation repository tests."""
import pytest

from app.repositories.conversation import ConversationRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_and_list_conversations(db_session):
    user_repo = UserRepository(db_session)
    user = await user_repo.create(
        UserCreate(email="chat@example.com", password="Password123"), password_hash="hashed"
    )
    repo = ConversationRepository(db_session)

    await repo.create(user.id, "Hello", "user")
    await repo.create(user.id, "Hi there", "coach")

    messages = await repo.list_for_user(user.id)
    assert len(messages) == 2
    assert messages[0].message_text == "Hello"


@pytest.mark.asyncio
async def test_update_and_delete_conversation(db_session):
    user_repo = UserRepository(db_session)
    user = await user_repo.create(
        UserCreate(email="conv-update@example.com", password="Password123"), password_hash="hashed"
    )
    repo = ConversationRepository(db_session)

    message = await repo.create(user.id, "Initial", "user")

    updated = await repo.update(message.id, message_text="Edited", sender_type="coach")
    assert updated is not None
    assert updated.message_text == "Edited"
    assert updated.sender_type == "coach"

    await repo.delete(message.id)
    assert await repo.get(message.id) is None
