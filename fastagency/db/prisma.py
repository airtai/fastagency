from contextlib import asynccontextmanager
from os import environ
from typing import Any, AsyncGenerator, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException
from prisma import Prisma  # type: ignore[attr-defined]
from prisma.actions import AuthTokenActions, ModelActions

from .base import BaseBackendProtocol, BaseFrontendProtocol


class PrismaBaseDB:
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


class PrismaBackendDB(BaseBackendProtocol, PrismaBaseDB):
    ENV_VAR = "PY_DATABASE_URL"

    async def find_model(self, model_uuid: Union[str, UUID]) -> Dict[str, Any]:
        model_uuid = str(model_uuid)
        async with self.get_db_connection() as db:
            model: Optional[Dict[str, Any]] = await db.query_first(
                'SELECT * from "Model" where uuid='  # nosec: [B608]
                + f"'{model_uuid}'"
            )
        if not model:
            raise HTTPException(
                status_code=404, detail="Something went wrong. Please try again later."
            )
        return model

    @asynccontextmanager
    async def get_model_connection(  # type: ignore[override]
        self,
    ) -> AsyncGenerator[ModelActions[Any], None]:
        async with self.get_db_connection() as db:
            yield db.model

    @asynccontextmanager
    async def get_authtoken_connection(  # type: ignore[override]
        self,
    ) -> AsyncGenerator[AuthTokenActions[Any], None]:
        async with self.get_db_connection() as db:
            yield db.authtoken


class PrismaFrontendDB(BaseFrontendProtocol, PrismaBaseDB):  # type: ignore[misc]
    ENV_VAR = "DATABASE_URL"

    async def get_user(self, user_uuid: Union[int, str]) -> Any:
        async with self.get_db_connection() as db:
            select_query = 'SELECT * from "User" where uuid=' + f"'{user_uuid}'"  # nosec: [B608]
            user = await db.query_first(
                select_query  # nosec: [B608]
            )
        if not user:
            raise HTTPException(
                status_code=404, detail=f"user_uuid {user_uuid} not found"
            )
        return user
