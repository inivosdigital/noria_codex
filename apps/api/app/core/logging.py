"""Logging configuration for structured output."""
import logging
from typing import Any, Dict


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logger for JSON-like structured output."""

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def log_event(event: str, **extra: Any) -> None:
    """Helper to emit structured logs."""

    payload: Dict[str, Any] = {"event": event, **extra}
    logging.getLogger("noria").info(payload)


__all__ = ["configure_logging", "log_event"]
