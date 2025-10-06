"""Domain-specific service errors."""


class DomainError(Exception):
    """Base domain error."""


class EmailAlreadyExistsError(DomainError):
    """Raised when attempting to create a user with an existing email."""


__all__ = ["DomainError", "EmailAlreadyExistsError"]
