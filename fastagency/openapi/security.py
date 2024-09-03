from pydantic import BaseModel
from typing import Literal, Type


class BaseSecurity(BaseModel):
    type: Literal["apiKey", "http", "mutualTLS" ,  "oauth2", "openIdConnect"]
    in_value: Literal["header", "query", "cookie"]
    name: str


class APIKeyHeader(BaseSecurity):
    type: Literal["apiKey"] = 'apiKey'
    in_value: Literal["header"] = "header"
    name: str = "X-API-KEY"

    @classmethod
    def get_parameter_cls(cls) -> Type[BaseModel]:
        return APIKeyHeaderParameters


class APIKeyHeaderParameters(BaseModel):
    value: str
    api_key_header: APIKeyHeader

    def add_security(self, q_params: dict, body_dict: dict) -> dict:
        if "headers" not in body_dict:
            body_dict["headers"] = {}
        body_dict["headers"][self.api_key_header.name] = self.value

        return q_params, body_dict
        

class APIKeyQuery(BaseSecurity):
    type: Literal["apiKey"] = 'apiKey'
    in_value: Literal["query"] = "query"
    name: str = "api_key"

    @classmethod
    def get_parameter_cls(cls) -> Type[BaseModel]:
        return APIKeyQueryParameters
    

class APIKeyQueryParameters(BaseModel):
    value: str
    api_key_query: APIKeyQuery

    def add_security(self, q_params: dict, body_dict: dict) -> dict:
        q_params[self.api_key_query.name] = self.value

        return q_params, body_dict
    

class APIKeyCookie(BaseSecurity):
    type: Literal["apiKey"] = 'apiKey'
    in_value: Literal["cookie"] = "cookie"
    name: str = "api_key"

    @classmethod
    def get_parameter_cls(cls) -> Type[BaseModel]:
        return APIKeyCookieParameters
    

class APIKeyCookieParameters(BaseModel):
    value: str
    api_key_cookie: APIKeyCookie

    def add_security(self, q_params: dict, body_dict: dict) -> dict:
        if "cookies" not in body_dict:
            body_dict["cookies"] = {}
        body_dict["cookies"][self.api_key_cookie.name] = self.value

        return q_params, body_dict


# Write a class with factory method which takes three parameters type, in_value, name and returns the appropriate class instance.
# The class should be named as SecurityFactory
# The factory method should be named as get_security
class SecurityFactory:
    @staticmethod
    def get_security(type: str, in_value: str, name: str) -> BaseSecurity:
        if type == "apiKey":
            if in_value == "header":
                return APIKeyHeader(name=name)
            elif in_value == "query":
                return APIKeyQuery(name=name)
            elif in_value == "cookie":
                return APIKeyCookie(name=name)
        else:
            raise ValueError("Invalid security type " + type)
