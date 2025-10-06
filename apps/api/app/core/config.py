"""Application configuration using Pydantic settings."""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    database_url: str = Field(alias="DATABASE_URL")
    supabase_service_role_key: Optional[str] = Field(default=None, alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_project_url: Optional[str] = Field(default=None, alias="SUPABASE_PROJECT_URL")
    password_pepper: str = Field(alias="PASSWORD_PEPPER")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    auth_signup_rate_limit: int = Field(default=10, alias="AUTH_SIGNUP_RATE_LIMIT", ge=1)
    auth_signup_rate_window_seconds: int = Field(
        default=60, alias="AUTH_SIGNUP_RATE_WINDOW_SECONDS", ge=1
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


__all__ = ["Settings", "get_settings"]
