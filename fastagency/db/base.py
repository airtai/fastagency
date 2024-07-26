from contextlib import asynccontextmanager
from os import environ
from typing import Any, AsyncGenerator, Dict, Optional, Protocol, runtime_checkable

from prisma import Prisma  # type: ignore[attr-defined]
from prisma.actions import AuthTokenActions, ModelActions


@runtime_checkable
class BaseProtocol(Protocol):
    @staticmethod
    async def get_db_url(env_var: str) -> str: ...

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_db_connection(self) -> AsyncGenerator[Prisma, None]: ...


@runtime_checkable
class BaseDBProtocol(Protocol):
    ENV_VAR: str

    @staticmethod
    async def get_db_url(env_var: str) -> str:
        db_url: Optional[str] = environ.get(env_var, None)
        if not db_url:
            raise ValueError(
                f"No database URL provided nor set as environment variable '{env_var}'"
            )
        if "connect_timeout" not in db_url:
            db_url += "?connect_timeout=60"
        return db_url

    @asynccontextmanager
    async def get_db_connection(self) -> AsyncGenerator[Prisma, None]:
        db_url = await self.get_db_url(self.ENV_VAR)
        db = Prisma(datasource={"url": db_url})
        await db.connect()
        try:
            yield db
        finally:
            await db.disconnect()


@runtime_checkable
class BaseBackendProtocol(BaseDBProtocol, Protocol):
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
class BaseFrontendProtocol(BaseDBProtocol, Protocol):
    async def get_user(self, user_uuid: str) -> Dict[str, Any]: ...
