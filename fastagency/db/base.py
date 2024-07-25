from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional, Union
from uuid import UUID

from prisma import Prisma  # type: ignore[attr-defined]


class BaseProtocol:
    @asynccontextmanager  # type: ignore[arg-type]
    async def get_db_connection(
        self, db_url: Optional[str] = None
    ) -> AsyncGenerator[Prisma, None]:
        raise NotImplementedError()

    async def get_wasp_db_url(self) -> str:
        raise NotImplementedError()

    async def find_model_using_raw(
        self, model_uuid: Union[str, UUID]
    ) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_user(self, user_uuid: Union[int, str]) -> Any:
        raise NotImplementedError()
