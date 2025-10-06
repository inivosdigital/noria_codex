"""Repository tests for user persistence."""
import pytest

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_and_get_user(db_session):
    repo = UserRepository(db_session)
    payload = UserCreate(email="user@example.com", password="Password123", goals={"focus": "stress"})
    created = await repo.create(payload, password_hash="hashed")

    assert created.email == payload.email
    fetched = await repo.get(created.id)
    assert fetched is not None
    assert fetched.id == created.id


@pytest.mark.asyncio
async def test_get_by_email(db_session):
    repo = UserRepository(db_session)
    payload = UserCreate(email="exists@example.com", password="Password123")
    await repo.create(payload, password_hash="hashed")

    existing = await repo.get_by_email(payload.email)
    assert existing is not None
    missing = await repo.get_by_email("missing@example.com")
    assert missing is None


@pytest.mark.asyncio
async def test_update_user(db_session):
    repo = UserRepository(db_session)
    payload = UserCreate(email="update@example.com", password="Password123", goals={"focus": "stress"})
    created = await repo.create(payload, password_hash="hashed")

    updated = await repo.update(
        created.id,
        email="new@example.com",
        goals={"focus": "sleep"},
        stage=2,
        password_hash="newhash",
    )

    assert updated is not None
    assert updated.email == "new@example.com"
    assert updated.goals == {"focus": "sleep"}
    assert updated.stage == 2
    assert updated.password_hash == "newhash"


@pytest.mark.asyncio
async def test_delete_user(db_session):
    repo = UserRepository(db_session)
    payload = UserCreate(email="delete@example.com", password="Password123")
    created = await repo.create(payload, password_hash="hashed")

    await repo.delete(created.id)
    remaining = await repo.get(created.id)
    assert remaining is None
