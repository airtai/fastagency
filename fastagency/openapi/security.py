from typing import Any, Dict, Literal, Protocol, Type

from pydantic import BaseModel, model_validator


class BaseSecurity(BaseModel):
    """Base class for security classes."""

    type: Literal["apiKey", "http", "mutualTLS", "oauth2", "openIdConnect"]
    in_value: Literal["header", "query", "cookie", "bearer", "basic", "tls"]
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


class BaseSecurityParameters(Protocol):
    """Base class for security parameters."""

    def apply(
        self,
        q_params: Dict[str, Any],
        body_dict: Dict[str, Any],
        security: BaseSecurity,
    ) -> None: ...

    def get_security_class(self) -> Type[BaseSecurity]: ...


class APIKeyHeader(BaseSecurity):
    """API Key Header security class."""

    type: Literal["apiKey"] = "apiKey"
    in_value: Literal["header"] = "header"

    class Parameters(BaseModel):  # BaseSecurityParameters
        """API Key Header security parameters class."""

        value: str

        def apply(
            self,
            q_params: Dict[str, Any],
            body_dict: Dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            api_key_header: APIKeyHeader = security  # type: ignore[assignment]

            if "headers" not in body_dict:
                body_dict["headers"] = {}

            body_dict["headers"][api_key_header.name] = self.value

        def get_security_class(self) -> Type[BaseSecurity]:
            return APIKeyHeader
