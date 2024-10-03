import logging
from typing import Any, ClassVar, Literal, Optional, Protocol, Union

from pydantic import BaseModel, model_validator

# Get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseSecurity(BaseModel):
    """Base class for security classes."""

    type: ClassVar[Literal["apiKey", "http", "mutualTLS", "oauth2", "openIdConnect"]]
    in_value: ClassVar[Literal["header", "query", "cookie", "bearer", "basic", "tls"]]
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
        }
        if self.in_value not in valid_in_values[self.type]:
            raise ValueError(
                f"Invalid in_value '{self.in_value}' for type '{self.type}'"
            )

    def accept(self, security_params: "BaseSecurityParameters") -> bool:
        return isinstance(self, security_params.get_security_class())

    @classmethod
    def is_supported(cls, type: str, in_value: Union[str, dict[str, Any]]) -> bool:
        return type == cls.type and in_value == cls.in_value

    @classmethod
    def get_security_class(cls, type: str, in_value: str) -> Optional[str]:
        sub_classes = cls.__subclasses__()

        for sub_class in sub_classes:
            if sub_class.is_supported(type, in_value):
                return sub_class.__name__
        else:
            logger.error(
                f"Unsupported type '{type}' and in_value '{in_value}' combination"
            )
            raise ValueError(
                f"Unsupported type '{type}' and in_value '{in_value}' combination"
            )


class BaseSecurityParameters(Protocol):
    """Base class for security parameters."""

    def apply(
        self,
        q_params: dict[str, Any],
        body_dict: dict[str, Any],
        security: BaseSecurity,
    ) -> None: ...

    def get_security_class(self) -> type[BaseSecurity]: ...


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

    @classmethod
    def is_supported(cls, type: str, in_value: Union[str, dict[str, Any]]) -> bool:
        return type == cls.type and isinstance(in_value, dict)

    class Parameters(BaseModel):  # BaseSecurityParameters
        """OAuth2 Password Bearer security class."""

        username: Optional[str] = None
        password: Optional[str] = None
        bearer_token: Optional[str] = None

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

        def apply(
            self,
            q_params: dict[str, Any],
            body_dict: dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            if not self.bearer_token:
                # request token from the tokenUrl with username and password
                raise NotImplementedError()

            if "headers" not in body_dict:
                body_dict["headers"] = {}

            body_dict["headers"]["Authorization"] = f"Bearer {self.bearer_token}"

        def get_security_class(self) -> type[BaseSecurity]:
            return OAuth2PasswordBearer
