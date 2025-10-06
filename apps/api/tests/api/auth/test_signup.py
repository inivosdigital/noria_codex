"""Signup API tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_user_service
from app.main import create_app
from app.services.user_service import UserService
from app.utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_signup_flow(db_session):
    app = create_app()

    async def override_user_service():
        return UserService(db_session)

    app.dependency_overrides[get_user_service] = override_user_service
    app.state.signup_rate_limiter = RateLimiter(limit=10, window_seconds=60)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "email": "new@example.com",
            "password": "Password123",
            "goals": {"aim": "resilience"},
            "stage": 1,
        }
        response = await client.post("/api/v1/auth/signup", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["user"]["email"] == payload["email"]

        duplicate = await client.post("/api/v1/auth/signup", json=payload)
        assert duplicate.status_code == 409

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_signup_rejects_weak_password(db_session):
    app = create_app()

    async def override_user_service():
        return UserService(db_session)

    app.dependency_overrides[get_user_service] = override_user_service
    app.state.signup_rate_limiter = RateLimiter(limit=10, window_seconds=60)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "email": "weak@example.com",
            "password": "alllowercase",
            "goals": None,
            "stage": 1,
        }
        response = await client.post("/api/v1/auth/signup", json=payload)
        assert response.status_code == 400
        assert "Password" in response.json()["detail"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_signup_rate_limit_enforced(db_session):
    app = create_app()

    async def override_user_service():
        return UserService(db_session)

    app.dependency_overrides[get_user_service] = override_user_service
    app.state.signup_rate_limiter = RateLimiter(limit=2, window_seconds=60)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "email": "limited@example.com",
            "password": "Password123",
            "goals": None,
            "stage": 1,
        }
        # First request succeeds
        response = await client.post("/api/v1/auth/signup", json=payload)
        assert response.status_code == 201

        # Update email to avoid duplicate conflict but count against rate limit
        payload["email"] = "limited2@example.com"
        response = await client.post("/api/v1/auth/signup", json=payload)
        assert response.status_code in {201, 409}

        payload["email"] = "limited3@example.com"
        response = await client.post("/api/v1/auth/signup", json=payload)
        assert response.status_code == 429

    app.dependency_overrides.clear()
