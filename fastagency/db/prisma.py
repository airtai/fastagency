from contextlib import asynccontextmanager
from datetime import datetime
from os import environ
from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List, Optional, Union
from uuid import UUID

from fastapi import HTTPException
from prisma import Prisma  # type: ignore[attr-defined]

from .base import BackendDBProtocol, DefaultDB, FrontendDBProtocol

if TYPE_CHECKING:
    from fastapi import FastAPI
    from faststream import ContextRepo


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


class PrismaBackendDB(BackendDBProtocol, PrismaBaseDB):
    ENV_VAR = "PY_DATABASE_URL"

    async def create_model(
        self,
        model_uuid: str,
        user_uuid: str,
        type_name: str,
        model_name: str,
        json_str: str,
    ) -> Dict[str, Any]:
        async with self._get_db_connection() as db:
            created_model = await db.model.create(
                data={
                    "uuid": model_uuid,
                    "user_uuid": user_uuid,
                    "type_name": type_name,
                    "model_name": model_name,
                    "json_str": json_str,  # type: ignore[typeddict-item]
                }
            )
        return created_model.model_dump()  # type: ignore[no-any-return]

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

    async def find_many_model(
        self, user_uuid: str, type_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        filters: Dict[str, Any] = {"user_uuid": user_uuid}
        if type_name:
            filters["type_name"] = type_name

        async with self._get_db_connection() as db:
            models = await db.model.find_many(where=filters)  # type: ignore[arg-type]
        return [model.model_dump() for model in models]

    async def update_model(
        self,
        model_uuid: str,
        user_uuid: str,
        type_name: str,
        model_name: str,
        json_str: str,
    ) -> Dict[str, Any]:
        async with self._get_db_connection() as db:
            updated_model = await db.model.update(
                where={"uuid": model_uuid},  # type: ignore[arg-type]
                data={  # type: ignore[typeddict-unknown-key]
                    "type_name": type_name,
                    "model_name": model_name,
                    "json_str": json_str,  # type: ignore[typeddict-item]
                    "user_uuid": user_uuid,
                },
            )
        return updated_model.model_dump()  # type: ignore[no-any-return,union-attr]

    async def delete_model(self, model_uuid: str) -> Dict[str, Any]:
        async with self._get_db_connection() as db:
            deleted_model = await db.model.delete(where={"uuid": model_uuid})
        return deleted_model.model_dump()  # type: ignore[no-any-return,union-attr]

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
        return created_auth_token.model_dump()  # type: ignore[no-any-return,union-attr]

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
        return deleted_auth_token.model_dump()  # type: ignore[no-any-return,union-attr]


class PrismaFrontendDB(FrontendDBProtocol, PrismaBaseDB):  # type: ignore[misc]
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

    async def _create_user(
        self, user_uuid: Union[int, str], email: str, username: str
    ) -> str:
        """Only to create user in testing."""
        async with self._get_db_connection() as db:
            insert_query = (
                'INSERT INTO "User" (email, username, uuid) VALUES ('  # nosec: [B608]
                + f"'{email}', '{username}', '{user_uuid}')"
            )
            await db.execute_raw(insert_query)

        return str(user_uuid)


@asynccontextmanager
async def _lifespan() -> AsyncGenerator[None, None]:
    prisma_backend_db = PrismaBackendDB()
    prisma_frontend_db = PrismaFrontendDB()

    with (
        DefaultDB.set(backend_db=prisma_backend_db, frontend_db=prisma_frontend_db),
    ):
        yield


@asynccontextmanager
async def fastapi_lifespan(app: "FastAPI") -> AsyncGenerator[None, None]:
    async with _lifespan():
        yield


@asynccontextmanager
async def faststream_lifespan(context: "ContextRepo") -> AsyncGenerator[None, None]:
    async with _lifespan():
        yield
