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
class BackendDBProtocol(Protocol):
    _default_db: Optional["BackendDBProtocol"] = None

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
    async def set_default(db: "BackendDBProtocol") -> AsyncGenerator[None, None]:
        old_default = BackendDBProtocol._default_db
        try:
            BackendDBProtocol._default_db = db
            yield
        finally:
            BackendDBProtocol._default_db = old_default

    @staticmethod
    async def get_default() -> "BackendDBProtocol":
        return BackendDBProtocol._default_db  # type: ignore[return-value]


@runtime_checkable
class FrontendDBProtocol(Protocol):
    _default_db: Optional["FrontendDBProtocol"] = None

    async def get_user(self, user_uuid: str) -> Dict[str, Any]: ...

    @staticmethod
    @asynccontextmanager
    async def set_default(db: "FrontendDBProtocol") -> AsyncGenerator[None, None]:
        old_default = FrontendDBProtocol._default_db
        try:
            FrontendDBProtocol._default_db = db
            yield
        finally:
            FrontendDBProtocol._default_db = old_default

    @staticmethod
    async def get_default() -> "FrontendDBProtocol":
        return FrontendDBProtocol._default_db  # type: ignore[return-value]
