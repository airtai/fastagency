import logging
from typing import Any, ClassVar, Literal, Optional, Protocol

import requests
from pydantic import BaseModel, model_validator
from typing_extensions import TypeAlias

# Get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BaseSecurityType: TypeAlias = type["BaseSecurity"]


class BaseSecurity(BaseModel):
    """Base class for security classes."""

    type: ClassVar[
        Literal["apiKey", "http", "mutualTLS", "oauth2", "openIdConnect", "unsupported"]
    ]
    in_value: ClassVar[
        Literal["header", "query", "cookie", "bearer", "basic", "tls", "unsupported"]
    ]
    name: str

    @model_validator(mode="after")  # type: ignore[misc]
    def __post_init__(
        self,
    ) -> None:  # dataclasses uses __post_init__ instead of model_validator
        """Validate the in_value based on the type."""
        valid_in_values = {
            "apiKey": ["header", "query", "cookie"],
            "http": ["bearer", "basic"],
            "oauth2": ["bearer"],
            "openIdConnect": ["bearer"],
            "mutualTLS": ["tls"],
            "unsupported": ["unsupported"],
        }
        if self.in_value not in valid_in_values[self.type]:
            raise ValueError(
                f"Invalid in_value '{self.in_value}' for type '{self.type}'"
            )

    def accept(self, security_params: "BaseSecurityParameters") -> bool:
        return isinstance(self, security_params.get_security_class())

    @classmethod
    def is_supported(cls, type: str, schema_parameters: dict[str, Any]) -> bool:
        return cls.type == type and cls.in_value == schema_parameters.get("in")

    @classmethod
    def get_security_class(
        cls, type: str, schema_parameters: dict[str, Any]
    ) -> BaseSecurityType:
        sub_classes = cls.__subclasses__()

        for sub_class in sub_classes:
            if sub_class.is_supported(type, schema_parameters):
                return sub_class

        logger.error(
            f"Unsupported type '{type}' and schema_parameters '{schema_parameters}' combination"
        )
        return UnsuportedSecurityStub

    @classmethod
    def get_security_parameters(cls, schema_parameters: dict[str, Any]) -> str:
        return f"{cls.__name__}(name=\"{schema_parameters.get('name')}\")"


class BaseSecurityParameters(Protocol):
    """Base class for security parameters."""

    def apply(
        self,
        q_params: dict[str, Any],
        body_dict: dict[str, Any],
        security: BaseSecurity,
    ) -> None: ...

    def get_security_class(self) -> type[BaseSecurity]: ...


class UnsuportedSecurityStub(BaseSecurity):
    """Unsupported security stub class."""

    type: ClassVar[Literal["unsupported"]] = "unsupported"
    in_value: ClassVar[Literal["unsupported"]] = "unsupported"

    @classmethod
    def is_supported(cls, type: str, schema_parameters: dict[str, Any]) -> bool:
        return False

    def accept(self, security_params: "BaseSecurityParameters") -> bool:
        if isinstance(self, security_params.get_security_class()):
            raise RuntimeError("Trying to set UnsuportedSecurityStub params")
        return False

    class Parameters(BaseModel):  # BaseSecurityParameters
        """API Key Header security parameters class."""

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            pass

        def get_security_class(self) -> type[BaseSecurity]:
            return UnsuportedSecurityStub


class APIKeyHeader(BaseSecurity):
    """API Key Header security class."""

    type: ClassVar[Literal["apiKey"]] = "apiKey"
    in_value: ClassVar[Literal["header"]] = "header"

    class Parameters(BaseModel):  # BaseSecurityParameters
        """API Key Header security parameters class."""

        value: str

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            api_key_header: APIKeyHeader = security  # type: ignore[assignment]

            if "headers" not in body_dict:
                body_dict["headers"] = {}

            body_dict["headers"][api_key_header.name] = self.value

        def get_security_class(self) -> type[BaseSecurity]:
            return APIKeyHeader


class APIKeyQuery(BaseSecurity):
    """API Key Query security class."""

    type: ClassVar[Literal["apiKey"]] = "apiKey"
    in_value: ClassVar[Literal["query"]] = "query"

    @classmethod
    def is_supported(cls, type: str, schema_parameters: dict[str, Any]) -> bool:
        return (
            super().is_supported(type, schema_parameters)
            and "name" in schema_parameters
        )

    class Parameters(BaseModel):  # BaseSecurityParameters
        """API Key Query security parameters class."""

        value: str

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            api_key_query: APIKeyQuery = security  # type: ignore[assignment]

            q_params[api_key_query.name] = self.value

        def get_security_class(self) -> type[BaseSecurity]:
            return APIKeyQuery


class APIKeyCookie(BaseSecurity):
    """API Key Cookie security class."""

    type: ClassVar[Literal["apiKey"]] = "apiKey"
    in_value: ClassVar[Literal["cookie"]] = "cookie"

    class Parameters(BaseModel):  # BaseSecurityParameters
        """API Key Cookie security parameters class."""

        value: str

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            api_key_cookie: APIKeyCookie = security  # type: ignore[assignment]

            if "cookies" not in body_dict:
                body_dict["cookies"] = {}

            body_dict["cookies"][api_key_cookie.name] = self.value

        def get_security_class(self) -> type[BaseSecurity]:
            return APIKeyCookie


class HTTPBearer(BaseSecurity):
    """HTTP Bearer security class."""

    type: ClassVar[Literal["http"]] = "http"
    in_value: ClassVar[Literal["bearer"]] = "bearer"

    @classmethod
    def is_supported(cls, type: str, schema_parameters: dict[str, Any]) -> bool:
        return cls.type == type and cls.in_value == schema_parameters.get("scheme")

    class Parameters(BaseModel):  # BaseSecurityParameters
        """HTTP Bearer security parameters class."""

        value: str

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            if "headers" not in body_dict:
                body_dict["headers"] = {}

            body_dict["headers"]["Authorization"] = f"Bearer {self.value}"

        def get_security_class(self) -> type[BaseSecurity]:
            return HTTPBearer


class OAuth2PasswordBearer(BaseSecurity):
    """OAuth2 Password Bearer security class."""

    type: ClassVar[Literal["oauth2"]] = "oauth2"
    in_value: ClassVar[Literal["bearer"]] = "bearer"
    token_url: str

    @classmethod
    def is_supported(cls, type: str, schema_parameters: dict[str, Any]) -> bool:
        return type == cls.type and "password" in schema_parameters.get("flows", {})

    @classmethod
    def get_security_parameters(cls, schema_parameters: dict[str, Any]) -> str:
        name = schema_parameters.get("name")
        token_url = f'{schema_parameters.get("server_url")}/{schema_parameters["flows"]["password"]["tokenUrl"]}'
        return f'{cls.__name__}(name="{name}", token_url="{token_url}")'

    class Parameters(BaseModel):  # BaseSecurityParameters
        """OAuth2 Password Bearer security class."""

        username: Optional[str] = None
        password: Optional[str] = None
        bearer_token: Optional[str] = None
        token_url: Optional[str] = None

        @model_validator(mode="before")
        def check_credentials(cls, values: dict[str, Any]) -> Any:  # noqa
            username = values.get("username")
            password = values.get("password")
            bearer_token = values.get("bearer_token")

            if not bearer_token and (not username or not password):
                # If bearer_token is not provided, both username and password must be defined
                raise ValueError(
                    "Both username and password are required if bearer_token is not provided."
                )

            return values

        def get_token(self, token_url: str) -> str:
            # Get the token
            request = requests.post(
                token_url,
                data={
                    "username": self.username,
                    "password": self.password,
                },
                timeout=5,
            )
            request.raise_for_status()
            return request.json()["access_token"]  # type: ignore

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            if not self.bearer_token:
                if security.token_url is None:  # type: ignore
                    raise ValueError("Token URL is not defined")
                self.bearer_token = self.get_token(security.token_url)  # type: ignore

            if "headers" not in body_dict:
                body_dict["headers"] = {}

            body_dict["headers"]["Authorization"] = f"Bearer {self.bearer_token}"

        def get_security_class(self) -> type[BaseSecurity]:
            return OAuth2PasswordBearer
