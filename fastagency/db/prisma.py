from contextlib import asynccontextmanager
from datetime import datetime
from os import environ
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from uuid import UUID

from fastapi import HTTPException
from prisma import Prisma  # type: ignore[attr-defined]
from prisma.actions import ModelActions

from .base import BaseBackendProtocol, BaseFrontendProtocol


class PrismaBaseDB:
    ENV_VAR: str

    @staticmethod
    async def _get_db_url(env_var: str) -> str:
        db_url: Optional[str] = environ.get(env_var, None)
        if not db_url:
            raise ValueError(
                f"No database URL provided nor set as environment variable '{env_var}'"
            )
        if "connect_timeout" not in db_url:
            db_url += "?connect_timeout=60"
        return db_url

    @asynccontextmanager
    async def _get_db_connection(self) -> AsyncGenerator[Prisma, None]:
        db_url = await self._get_db_url(self.ENV_VAR)
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
        async with self._get_db_connection() as db:
            model: Optional[Dict[str, Any]] = await db.query_first(
                'SELECT * from "Model" where uuid='  # nosec: [B608]
                + f"'{model_uuid}'"
            )
        if not model:
            raise HTTPException(
                status_code=404, detail="Something went wrong. Please try again later."
            )
        return model

    async def delete_model(self, model_uuid: str) -> Dict[str, Any]:
        async with self._get_db_connection() as db:
            deleted_model = await db.model.delete(where={"uuid": model_uuid})
        return deleted_model.model_dump()

    async def create_auth_token(
        self,
        auth_token_uuid: str,
        name: str,
        user_uuid: str,
        deployment_uuid: str,
        hashed_auth_token: str,
        expiry: str,
        expires_at: datetime,
    ) -> Dict[str, Any]:
        async with self._get_db_connection() as db:
            created_auth_token = await db.authtoken.create(  # type: ignore[attr-defined]
                data={
                    "uuid": auth_token_uuid,
                    "name": name,
                    "user_uuid": user_uuid,
                    "deployment_uuid": deployment_uuid,
                    "auth_token": hashed_auth_token,
                    "expiry": expiry,
                    "expires_at": expires_at,
                }
            )
        return created_auth_token.model_dump()

    async def find_many_auth_token(
        self, user_uuid: str, deployment_uuid: str
    ) -> List[Dict[str, Any]]:
        async with self._get_db_connection() as db:
            auth_tokens = await db.authtoken.find_many(
                where={"deployment_uuid": deployment_uuid, "user_uuid": user_uuid},
            )
        return [auth_token.model_dump() for auth_token in auth_tokens]

    async def delete_auth_token(
        self, auth_token_uuid: str, deployment_uuid: str, user_uuid: str
    ) -> Dict[str, Any]:
        async with self._get_db_connection() as db:
            deleted_auth_token = await db.authtoken.delete(
                where={  # type: ignore[typeddict-unknown-key]
                    "uuid": auth_token_uuid,
                    "deployment_uuid": deployment_uuid,
                    "user_uuid": user_uuid,
                },
            )
        return deleted_auth_token.model_dump()

    @asynccontextmanager
    async def get_model_connection(  # type: ignore[override]
        self,
    ) -> AsyncGenerator[ModelActions[Any], None]:
        async with self._get_db_connection() as db:
            yield db.model


class PrismaFrontendDB(BaseFrontendProtocol, PrismaBaseDB):  # type: ignore[misc]
    ENV_VAR = "DATABASE_URL"

    async def get_user(self, user_uuid: Union[int, str]) -> Any:
        async with self._get_db_connection() as db:
            select_query = 'SELECT * from "User" where uuid=' + f"'{user_uuid}'"  # nosec: [B608]
            user = await db.query_first(
                select_query  # nosec: [B608]
            )
        if not user:
            raise HTTPException(
                status_code=404, detail=f"user_uuid {user_uuid} not found"
            )
        return user
