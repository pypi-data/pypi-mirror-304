"""Ready-to-use and customizable users management for FastAPI."""

__version__ = "13.0.0"

from fastapi_users_with_username import models, schemas  # noqa: F401
from fastapi_users_with_username.exceptions import InvalidID, InvalidPasswordException
from fastapi_users_with_username.fastapi_users_with_username import FastAPIUsers  # noqa: F401
from fastapi_users_with_username.manager import (  # noqa: F401
    BaseUserManager,
    IntegerIDMixin,
    UUIDIDMixin,
)

__all__ = [
    "models",
    "schemas",
    "FastAPIUsers",
    "BaseUserManager",
    "InvalidPasswordException",
    "InvalidID",
    "UUIDIDMixin",
    "IntegerIDMixin",
]
