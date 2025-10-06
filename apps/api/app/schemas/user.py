"""Pydantic schemas for user resources."""
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    goals: Optional[dict[str, Any]] = None
    stage: int = Field(default=1, ge=1, le=3)


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    goals: Optional[dict[str, Any]] = None
    stage: int
    created_at: datetime


class SignupResponse(BaseModel):
    user: UserRead
    message: str


__all__ = ["UserCreate", "UserRead", "SignupResponse"]
