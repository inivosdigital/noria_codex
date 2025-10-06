"""User repository encapsulating database operations."""
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate


class UserRepository(BaseRepository):
    """CRUD helpers for user entities."""

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, payload: UserCreate, password_hash: str) -> User:
        user = User(
            email=payload.email,
            password_hash=password_hash,
            goals=payload.goals,
            stage=payload.stage,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: UUID, **fields: Any) -> Optional[User]:
        """Update mutable user fields and return the fresh entity."""

        allowed = {"email", "password_hash", "goals", "stage"}
        updates = {key: value for key, value in fields.items() if key in allowed and value is not None}
        if not updates:
            return await self.get(user_id)

        user = await self.get(user_id)
        if user is None:
            return None

        for key, value in updates.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        user = await self.get(user_id)
        if user is None:
            return
        await self.session.delete(user)
        await self.session.commit()


__all__ = ["UserRepository"]
