from typing import Any, Dict, Literal, Protocol, Type

from pydantic import BaseModel


class BaseSecurity(BaseModel):
    """Base class for security classes."""

    type: Literal["apiKey", "http", "mutualTLS", "oauth2", "openIdConnect"]
    in_value: Literal["header", "query", "cookie", "bearer", "basic", "tls"]
    name: str

    def __post_init__(self):
        if self.type == "apiKey":
            if self.in_value not in ["header", "query", "cookie"]:
                raise ValueError("Invalid in_value for apiKey")
        elif self.type == "http":
            if self.in_value not in ["bearer", "basic"]:
                raise ValueError("Invalid in_value for http")
        elif self.type == "oauth2":
            if self.in_value not in ["bearer"]:
                raise ValueError("Invalid in_value for oauth2")
        elif self.type == "openIdConnect":
            if self.in_value not in ["bearer"]:
                raise ValueError("Invalid in_value for openIdConnect")
        elif self.type == "mutualTLS":
            if self.in_value not in ["tls"]:
                raise ValueError("Invalid in_value for mutualTLS")


class BaseSecurityParameters(Protocol):
    """Base class for security parameters."""

    def add_security(
        self,
        q_params: Dict[str, Any],
        body_dict: Dict[str, Any],
        security: BaseSecurity,
    ) -> None: ...

    def get_security(self) -> Type[BaseSecurity]: ...


class APIKeyHeader(BaseSecurity):
    """API Key Header security class."""

    type: Literal["apiKey"] = "apiKey"
    in_value: Literal["header"] = "header"

    class Parameters(BaseModel):  # BaseSecurityParameters
        """API Key Header security parameters class."""

        value: str

        def add_security(
            self,
            q_params: Dict[str, Any],
            body_dict: Dict[str, Any],
            security: BaseSecurity,
        ) -> None:
            api_key_header: APIKeyHeader = security

            if "headers" not in body_dict:
                body_dict["headers"] = {}

            body_dict["headers"][api_key_header.name] = self.value

        def get_security(self) -> Type[BaseSecurity]:
            return APIKeyHeader


# class APIKeyQuery(BaseSecurity):
#     type: Literal["apiKey"] = "apiKey"
#     in_value: Literal["query"] = "query"
#     name: str = "api_key"

#     @classmethod
#     def get_parameter_cls(cls) -> Type[BaseModel]:
#         return APIKeyQueryParameters


# class APIKeyQueryParameters(BaseModel):
#     value: str
#     api_key_query: APIKeyQuery

#     def add_security(self, q_params: dict, body_dict: dict) -> dict:
#         q_params[self.api_key_query.name] = self.value

#         return q_params, body_dict


# class APIKeyCookie(BaseSecurity):
#     type: Literal["apiKey"] = "apiKey"
#     in_value: Literal["cookie"] = "cookie"
#     name: str = "api_key"

#     @classmethod
#     def get_parameter_cls(cls) -> Type[BaseModel]:
#         return APIKeyCookieParameters


# class APIKeyCookieParameters(BaseModel):
#     value: str
#     api_key_cookie: APIKeyCookie

#     def add_security(self, q_params: dict, body_dict: dict) -> dict:
#         if "cookies" not in body_dict:
#             body_dict["cookies"] = {}
#         body_dict["cookies"][self.api_key_cookie.name] = self.value

#         return q_params, body_dict


# # Write a class with factory method which takes three parameters type, in_value, name and returns the appropriate class instance.
# # The class should be named as SecurityFactory
# # The factory method should be named as get_security
# class SecurityFactory:
#     @staticmethod
#     def get_security(type: str, in_value: str, name: str) -> BaseSecurity:
#         if type == "apiKey":
#             if in_value == "header":
#                 return APIKeyHeader(name=name)
#             elif in_value == "query":
#                 return APIKeyQuery(name=name)
#             elif in_value == "cookie":
#                 return APIKeyCookie(name=name)
#         else:
#             raise ValueError("Invalid security type " + type)
