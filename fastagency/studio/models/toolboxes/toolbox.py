from typing import Annotated, Any, Optional, Union
from uuid import UUID

import httpx
from pydantic import AfterValidator, Field, HttpUrl
from typing_extensions import TypeAlias

from ....openapi.client import Client
from ..base import Model
from ..registry import Registry

# Pydantic adds trailing slash automatically to URLs, so we need to remove it
# https://github.com/pydantic/pydantic/issues/7186#issuecomment-1691594032
URL = Annotated[HttpUrl, AfterValidator(lambda x: str(x).rstrip("/"))]

__all__ = [
    "Client",
    "OpenAPIAuthToken",
    "OpenAPIAuth",
    "Toolbox",
]


@Registry.get_default().register("secret")
class OpenAPIAuthToken(Model):
    token: Annotated[
        str,
        Field(
            description="Authentication token for OpenAPI routes",
        ),
    ]

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> tuple[str, str]:
        raise RuntimeError("This method should never be called.")


OpenAPIAuthTokenRef: TypeAlias = OpenAPIAuthToken.get_reference_model()  # type: ignore[valid-type]


@Registry.get_default().register("secret")
class OpenAPIAuth(Model):
    username: Annotated[
        str,
        Field(
            description="Username for OpenAPI routes authentication",
        ),
    ]
    password: Annotated[
        str,
        Field(
            description="Password for OpenAPI routes authentication",
        ),
    ]

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> tuple[str, str]:
        raise RuntimeError("This method should never be called.")


OpenAPIAuthRef: TypeAlias = OpenAPIAuth.get_reference_model()  # type: ignore[valid-type]


@Registry.get_default().register("toolbox")
class Toolbox(Model):
    openapi_url: Annotated[
        URL,
        Field(
            title="OpenAPI URL",
            description="The URL of OpenAPI specification file",
        ),
    ]
    openapi_auth: Annotated[
        Optional[Union[OpenAPIAuthTokenRef, OpenAPIAuthRef]],
        Field(
            title="OpenAPI Auth",
            description="Authentication information for the API mentioned in the OpenAPI specification",
        ),
    ] = None

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> Client:
        my_model = await cls.from_db(model_id)

        # Download OpenAPI spec
        with httpx.Client() as httpx_client:
            response = httpx_client.get(my_model.openapi_url)  # type: ignore[arg-type]
            response.raise_for_status()
            openapi_spec = response.text

        client = Client.create(openapi_spec)

        return client


ToolboxRef: TypeAlias = Toolbox.get_reference_model()  # type: ignore[valid-type]