from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Optional,
    Protocol,
    runtime_checkable,
)

from prisma import Prisma  # type: ignore[attr-defined]
from prisma.actions import AuthTokenActions, ModelActions


@runtime_checkable
class BaseProtocol(Protocol):
    @staticmethod
    async def get_db_url(env_var: str) -> str: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_db_connection(self) -> AsyncGenerator[Prisma, None]: ...


@runtime_checkable
class BaseBackendProtocol(Protocol):
    async def find_model(self, model_uuid: str) -> Dict[str, Any]: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_model_connection(
        self,
    ) -> AsyncGenerator[ModelActions[Any], None]: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_authtoken_connection(
        self,
    ) -> AsyncGenerator[AuthTokenActions[Any], None]: ...


@runtime_checkable
class BaseFrontendProtocol(Protocol):
    _default_db: Optional["BaseFrontendProtocol"] = None

    async def get_user(self, user_uuid: str) -> Dict[str, Any]: ...

    @staticmethod
    @asynccontextmanager
    async def set_default(db: "BaseFrontendProtocol") -> AsyncGenerator[None, None]:
        old_default = BaseFrontendProtocol._default_db
        try:
            BaseFrontendProtocol._default_db = db
            yield
        finally:
            BaseFrontendProtocol._default_db = old_default

    @staticmethod
    async def get_default() -> Optional["BaseFrontendProtocol"]:
        return BaseFrontendProtocol._default_db
