"""FastAPI dependency providers."""
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.utils.rate_limiter import RateLimiter
from app.services.analysis_service import AnalysisService
from app.services.conversation_service import ConversationService
from app.services.user_service import UserService


async def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(session)


async def get_conversation_service(session: AsyncSession = Depends(get_db_session)) -> ConversationService:
    return ConversationService(session)


async def get_analysis_service(session: AsyncSession = Depends(get_db_session)) -> AnalysisService:
    return AnalysisService(session)


async def get_signup_rate_limiter(request: Request) -> RateLimiter:
    return request.app.state.signup_rate_limiter


__all__ = [
    "get_user_service",
    "get_conversation_service",
    "get_analysis_service",
    "get_signup_rate_limiter",
]
