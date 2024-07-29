from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Optional,
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class BaseBackendProtocol(Protocol):
    _default_db: Optional["BaseBackendProtocol"] = None

    async def find_model(self, model_uuid: str) -> Dict[str, Any]: ...
    async def delete_model(self, model_uuid: str) -> Dict[str, Any]: ...

    @staticmethod
    @asynccontextmanager
    async def set_default(db: "BaseBackendProtocol") -> AsyncGenerator[None, None]:
        old_default = BaseBackendProtocol._default_db
        try:
            BaseBackendProtocol._default_db = db
            yield
        finally:
            BaseBackendProtocol._default_db = old_default

    @staticmethod
    async def get_default() -> Optional["BaseBackendProtocol"]:
        return BaseBackendProtocol._default_db


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
