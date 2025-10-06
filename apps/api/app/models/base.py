"""Declarative base for SQLAlchemy models."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class."""

    pass


__all__ = ["Base"]
