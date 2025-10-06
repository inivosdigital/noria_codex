"""FastAPI application factory."""
from fastapi import FastAPI

from app.api.v1.auth.routes import router as auth_router
from app.core.config import get_settings
from app.core.database import verify_database_connection
from app.core.logging import configure_logging
from app.utils.rate_limiter import RateLimiter


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = get_settings()
    configure_logging()
    app = FastAPI(title="Noria API", version="0.1.0", docs_url="/docs")

    app.state.signup_rate_limiter = RateLimiter(
        settings.auth_signup_rate_limit,
        settings.auth_signup_rate_window_seconds,
    )

    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

    @app.get("/health", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    @app.on_event("startup")
    async def startup_event() -> None:  # pragma: no cover - wire-up code
        await verify_database_connection()

    return app


app = create_app()
