from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Coroutine, Any, Optional
from uuid import UUID

from fastapi import APIRouter


class AuthStrategy(ABC):
    authorize_response_model: Any

    def authorize(self, user) -> Any: ...


class AuthBackend(ABC):

    strategy: "AuthStrategy"

    @abstractmethod
    def authorize(self, user: "BaseUser") -> Any: ...

    @abstractmethod
    def authenticate(self) -> Callable[[], Coroutine[Any, Any, None]]: ...

    @abstractmethod
    def auth_required(self) -> Callable[[], Coroutine[Any, Any, None]]: ...

    @abstractmethod
    def with_permissions(self, *permissions: tuple[str, str]) -> Callable[[], Coroutine[Any, Any, None]]: ...

    def create_router(self, **kwargs) -> APIRouter: ...


class BaseUser:
    id: int
    uuid: UUID
    username: Optional[str]
    email: Optional[str]
    password_hash: str
    password_change_dt: datetime
    password_salt: str
    is_superuser: bool
    is_active: bool
    is_verified: bool
    created_at: datetime
    EMAIL_FIELD: str
    AUTH_FIELDS: tuple[str, ...]

    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    @property
    def display_name(self) -> str:
        raise NotImplementedError()

    @property
    def is_simple(self) -> bool:
        raise NotImplementedError()

    def has_permissions(self, *permissions) -> tuple[str, str]:
        raise NotImplementedError()


class SimpleUser(BaseUser):
    pk: Any

    def __init__(self, pk: int | UUID | str, username: str):
        self.pk = pk
        self.username = username

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def is_simple(self) -> bool:
        return True


class UnauthenticatedUser(BaseUser):
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ""

    def is_simple(self) -> bool:
        return True
