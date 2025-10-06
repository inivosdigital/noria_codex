"""Security utilities for authentication flows."""
import re
from typing import Final

from passlib.context import CryptContext

from .config import get_settings


_PASSWORD_POLICY: Final[re.Pattern[str]] = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False,
)


def validate_password_requirements(password: str) -> None:
    """Ensure password meets policy requirements."""

    if not _PASSWORD_POLICY.match(password):
        raise ValueError(
            "Password must be at least 8 characters and include upper, lower, and numeric characters."
        )


def hash_password(password: str) -> str:
    """Hash password with pepper applied."""

    settings = get_settings()
    salted = f"{password}{settings.password_pepper}"
    return _pwd_context.hash(salted)


def verify_password(password: str, hashed: str) -> bool:
    """Validate password against stored hash."""

    settings = get_settings()
    salted = f"{password}{settings.password_pepper}"
    return _pwd_context.verify(salted, hashed)


__all__ = ["validate_password_requirements", "hash_password", "verify_password"]
