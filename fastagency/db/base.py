from contextlib import asynccontextmanager
from datetime import datetime
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Optional,
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class BaseBackendProtocol(Protocol):
    _default_db: Optional["BaseBackendProtocol"] = None

    async def create_model(
        self,
        model_uuid: str,
        user_uuid: str,
        type_name: str,
        model_name: str,
        json_str: str,
    ) -> Dict[str, Any]: ...
    async def find_model(self, model_uuid: str) -> Dict[str, Any]: ...
    async def find_many_model(
        self, user_uuid: str, type_name: Optional[str] = None
    ) -> List[Dict[str, Any]]: ...
    async def update_model(
        self,
        model_uuid: str,
        user_uuid: str,
        type_name: str,
        model_name: str,
        json_str: str,
    ) -> Dict[str, Any]: ...
    async def delete_model(self, model_uuid: str) -> Dict[str, Any]: ...

    async def create_auth_token(
        self,
        auth_token_uuid: str,
        name: str,
        user_uuid: str,
        deployment_uuid: str,
        hashed_auth_token: str,
        expiry: str,
        expires_at: datetime,
    ) -> Dict[str, Any]: ...
    async def find_many_auth_token(
        self, user_uuid: str, deployment_uuid: str
    ) -> List[Dict[str, Any]]: ...
    async def delete_auth_token(
        self, auth_token_uuid: str, deployment_uuid: str, user_uuid: str
    ) -> Dict[str, Any]: ...

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
    async def get_default() -> "BaseBackendProtocol":
        return BaseBackendProtocol._default_db  # type: ignore[return-value]


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
    async def get_default() -> "BaseFrontendProtocol":
        return BaseFrontendProtocol._default_db  # type: ignore[return-value]
