import re
from typing import Annotated, Any, Dict, Literal, Type
from uuid import UUID

from pydantic import AfterValidator, Field, HttpUrl, field_validator
from typing_extensions import TypeAlias

from ..base import Model
from ..registry import register

OpenAIModels: TypeAlias = Literal[
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
    "gpt-4o-2024-05-13",
    "gpt-4-32k",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-turbo-preview",
    "gpt-4-0125-preview",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-4-1106-vision-preview",
    "gpt-4-0613",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-1106",
    #    "gpt-3.5-turbo-instruct"  Compatible with legacy Completions endpoint and not Chat Completions.
]

__all__ = [
    "OpenAIAPIKey",
    "OpenAI",
]


@register("secret")
class OpenAIAPIKey(Model):
    api_key: Annotated[
        str,
        Field(
            description="The API Key from OpenAI",
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model: OpenAIAPIKey = await cls.from_db(model_id)

        return my_model.api_key

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls: Type["OpenAIAPIKey"], value: Any) -> Any:
        if not re.match(r"^sk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20}$", value):
            raise ValueError("Invalid OpenAI API Key")
        return value


OpenAIAPIKeyRef: TypeAlias = OpenAIAPIKey.get_reference_model()  # type: ignore[valid-type]

# Pydantic adds trailing slash automatically to URLs, so we need to remove it
# https://github.com/pydantic/pydantic/issues/7186#issuecomment-1691594032
URL = Annotated[HttpUrl, AfterValidator(lambda x: str(x).rstrip("/"))]


@register("llm")
class OpenAI(Model):
    model: Annotated[  # type: ignore[valid-type]
        OpenAIModels,
        Field(description="The model to use for the OpenAI API, e.g. 'gpt-3.5-turbo'"),
    ] = "gpt-3.5-turbo"

    api_key: OpenAIAPIKeyRef

    base_url: Annotated[URL, Field(description="The base URL of the OpenAI API")] = URL(
        url="https://api.openai.com/v1"
    )

    api_type: Annotated[
        Literal["openai"],
        Field(title="API Type", description="The type of the API, must be 'openai'"),
    ] = "openai"

    temperature: Annotated[
        float,
        Field(
            description="The temperature to use for the model, must be between 0 and 2",
            ge=0.0,
            le=2.0,
        ),
    ] = 0.8

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> Dict[str, Any]:
        my_model: OpenAI = await cls.from_db(model_id)

        api_key_model: OpenAIAPIKey = await my_model.api_key.get_data_model().from_db(
            my_model.api_key.uuid
        )

        api_key = await api_key_model.create_autogen(my_model.api_key.uuid, user_id)

        config_list = [
            {
                "model": my_model.model,
                "api_key": api_key,
                "base_url": str(my_model.base_url),
                "api_type": my_model.api_type,
            }
        ]

        llm_config = {
            "config_list": config_list,
            "temperature": my_model.temperature,
        }

        return llm_config
