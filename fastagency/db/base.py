from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Protocol,
    runtime_checkable,
)

from prisma import Prisma  # type: ignore[attr-defined]
from prisma.actions import AuthTokenActions, ModelActions


@runtime_checkable
class BaseProtocol(Protocol):
    @staticmethod
    async def get_db_url() -> str: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_db_connection(self) -> AsyncGenerator[Prisma, None]: ...


@runtime_checkable
class BaseBackendProtocol(BaseProtocol, Protocol):
    async def find_model_using_raw(self, model_uuid: str) -> Dict[str, Any]: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_model_connection(
        self,
    ) -> AsyncGenerator[ModelActions[Any], None]: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_authtoken_connection(
        self,
    ) -> AsyncGenerator[AuthTokenActions[Any], None]: ...


@runtime_checkable
class BaseFrontendProtocol(BaseProtocol, Protocol):
    async def get_user(self, user_uuid: str) -> Dict[str, Any]: ...
