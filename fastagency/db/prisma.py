from contextlib import asynccontextmanager
from os import environ
from typing import Any, AsyncGenerator, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException
from prisma import Prisma  # type: ignore[attr-defined]

from .base import BaseProtocol


class BackendDBProtocol(BaseProtocol):
    async def get_db_url(self) -> str:
        db_url: str = environ.get("PY_DATABASE_URL", None)  # type: ignore[assignment,arg-type]
        if not db_url:
            raise ValueError(
                "No database URL provided nor set as environment variable 'PY_DATABASE_URL'"
            )  # pragma: no cover
        if "connect_timeout" not in db_url:
            db_url += "?connect_timeout=60"
        return db_url

    @asynccontextmanager
    async def get_db_connection(  # type: ignore[override]
        self,
    ) -> AsyncGenerator[Prisma, None]:
        db_url = await self.get_db_url()
        db = Prisma(datasource={"url": db_url})
        await db.connect()
        try:
            yield db
        finally:
            await db.disconnect()

    async def find_model_using_raw(
        self, model_uuid: Union[str, UUID]
    ) -> Dict[str, Any]:
        if isinstance(model_uuid, UUID):
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


class FrontendDBProtocol(BaseProtocol):
    async def get_db_url(self) -> str:
        db_url: str = environ.get("DATABASE_URL", None)  # type: ignore[assignment,arg-type]
        if not db_url:
            raise ValueError(
                "No database URL provided nor set as environment variable 'DATABASE_URL'"
            )  # pragma: no cover
        if "connect_timeout" not in db_url:
            db_url += "?connect_timeout=60"
        return db_url

    @asynccontextmanager
    async def get_db_connection(  # type: ignore[override]
        self,
    ) -> AsyncGenerator[Prisma, None]:
        db_url = await self.get_db_url()
        db = Prisma(datasource={"url": db_url})
        await db.connect()
        try:
            yield db
        finally:
            await db.disconnect()

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
