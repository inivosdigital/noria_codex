"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.dependencies import get_signup_rate_limiter, get_user_service
from app.schemas.user import SignupResponse, UserCreate, UserRead
from app.services.exceptions import EmailAlreadyExistsError
from app.services.user_service import UserService
from app.utils.rate_limiter import RateLimiter

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    payload: UserCreate,
    request: Request,
    service: UserService = Depends(get_user_service),
    limiter: RateLimiter = Depends(get_signup_rate_limiter),
) -> SignupResponse:
    """Create a new user using the provided credentials.

    Enforces a per-client rate limit (default: 10 requests per minute) to mitigate brute force
    attacks against the signup endpoint.
    """

    client_host = request.client.host if request.client else "unknown"
    allowed = await limiter.allow(client_host)
    if not allowed:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many signup attempts. Try again later.")

    try:
        user = await service.register_user(payload)
    except EmailAlreadyExistsError as exc:  # pragma: no cover - thin handler
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return SignupResponse(
        user=UserRead.model_validate(user, from_attributes=True),
        message="Account created",
    )


__all__ = ["router"]
