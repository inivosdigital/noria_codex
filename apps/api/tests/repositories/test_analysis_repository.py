"""Analysis repository tests."""
import pytest

from app.repositories.analysis import AnalysisRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_and_list_analysis_results(db_session):
    user_repo = UserRepository(db_session)
    user = await user_repo.create(
        UserCreate(email="analysis@example.com", password="Password123"), password_hash="hashed"
    )
    repo = AnalysisRepository(db_session)

    await repo.create(user.id, chat_score=75, message_range="1-5")
    await repo.create(user.id, chat_score=80, message_range="6-10")

    results = await repo.list_for_user(user.id)
    assert len(results) == 2
    assert results[0].chat_score == 75


@pytest.mark.asyncio
async def test_update_and_delete_analysis_result(db_session):
    user_repo = UserRepository(db_session)
    user = await user_repo.create(
        UserCreate(email="analysis-update@example.com", password="Password123"), password_hash="hashed"
    )
    repo = AnalysisRepository(db_session)

    result = await repo.create(user.id, chat_score=70, message_range="1-3")
    updated = await repo.update(result.id, chat_score=85, message_range="5-7")

    assert updated is not None
    assert updated.chat_score == 85
    assert updated.message_range == "5-7"

    await repo.delete(result.id)
    assert await repo.get(result.id) is None
