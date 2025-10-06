"""User service orchestrating repository operations."""
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, validate_password_requirements
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.exceptions import EmailAlreadyExistsError


class UserService:
    """Business logic for user management."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepository(session)

    async def register_user(self, payload: UserCreate):
        validate_password_requirements(payload.password)
        existing = await self._users.get_by_email(payload.email)
        if existing:
            raise EmailAlreadyExistsError("Email already registered")
        password_hash = hash_password(payload.password)
        user = await self._users.create(payload, password_hash)
        return user

    async def get_user(self, user_id):
        return await self._users.get(user_id)

    async def update_user(
        self,
        user_id: UUID,
        *,
        email: str | None = None,
        password: str | None = None,
        goals: dict[str, Any] | None = None,
        stage: int | None = None,
    ):
        updates: dict[str, Any] = {}

        if email is not None:
            existing = await self._users.get_by_email(email)
            if existing and existing.id != user_id:
                raise EmailAlreadyExistsError("Email already registered")
            updates["email"] = email

        if password is not None:
            validate_password_requirements(password)
            updates["password_hash"] = hash_password(password)

        if goals is not None:
            updates["goals"] = goals

        if stage is not None:
            updates["stage"] = stage

        return await self._users.update(user_id, **updates)

    async def delete_user(self, user_id: UUID) -> None:
        await self._users.delete(user_id)


__all__ = ["UserService"]
