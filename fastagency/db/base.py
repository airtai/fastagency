from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict

from prisma import Prisma  # type: ignore[attr-defined]
from prisma.actions import AuthTokenActions, ModelActions


class BaseProtocol:
    async def get_db_url(self) -> str:
        raise NotImplementedError()

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_db_connection(self) -> AsyncGenerator[Prisma, None]:
        raise NotImplementedError()


class BaseBackendProtocol(BaseProtocol):
    async def find_model_using_raw(self, model_uuid: str) -> Dict[str, Any]:
        raise NotImplementedError()

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_model_connection(
        self,
    ) -> AsyncGenerator[ModelActions[Any], None]:
        raise NotImplementedError()

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_authtoken_connection(
        self,
    ) -> AsyncGenerator[AuthTokenActions[Any], None]:
        raise NotImplementedError()


class BaseFrontendProtocol(BaseProtocol):
    async def get_user(self, user_uuid: str) -> Dict[str, Any]:
        raise NotImplementedError()
