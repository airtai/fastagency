from contextlib import asynccontextmanager
from typing import AsyncGenerator

from prisma import Prisma  # type: ignore[attr-defined]


class BaseProtocol:
    async def get_db_url(self) -> str:
        raise NotImplementedError()

    @asynccontextmanager  # type: ignore[arg-type]
    async def get_db_connection(self) -> AsyncGenerator[Prisma, None]:
        raise NotImplementedError()
