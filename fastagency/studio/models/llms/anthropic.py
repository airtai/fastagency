import re
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AfterValidator, Field, HttpUrl, field_validator
from typing_extensions import TypeAlias

from ..base import Model
from ..registry import register

AnthropicModels: TypeAlias = Literal[
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

__all__ = [
    "AnthropicAPIKey",
    "Anthropic",
]


@register("secret")
class AnthropicAPIKey(Model):
    api_key: Annotated[
        str,
        Field(
            title="API Key",
            description="The API Key from Anthropic",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "The API key specified here will be used to authenticate requests to Anthropic services."
                }
            },
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model: AnthropicAPIKey = await cls.from_db(model_id)

        return my_model.api_key

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls: type["AnthropicAPIKey"], value: Any) -> Any:
        if not re.match(r"^sk-ant-api03-[a-zA-Z0-9\-\_]{95}$", value):
            raise ValueError("Invalid Anthropic API Key")
        return value


AnthropicAPIKeyRef: TypeAlias = AnthropicAPIKey.get_reference_model()  # type: ignore[valid-type]

# Pydantic adds trailing slash automatically to URLs, so we need to remove it
# https://github.com/pydantic/pydantic/issues/7186#issuecomment-1691594032
URL = Annotated[HttpUrl, AfterValidator(lambda x: str(x).rstrip("/"))]


@register("llm")
class Anthropic(Model):
    model: Annotated[  # type: ignore[valid-type]
        AnthropicModels,
        Field(
            description="The model to use for the Anthropic API, e.g. 'claude-3-5-sonnet-20240620'",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Choose the model that the LLM should use to generate responses."
                }
            },
        ),
    ] = "claude-3-5-sonnet-20240620"

    api_key: Annotated[
        AnthropicAPIKeyRef,
        Field(
            title="API Key",
            description="The API Key from Anthropic",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Choose the API key that will be used to authenticate requests to Anthropic services."
                }
            },
        ),
    ]

    base_url: Annotated[
        URL,
        Field(
            title="Base URL",
            description="The base URL of the Anthropic API",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "The base URL that the LLM uses to interact with Anthropic services."
                }
            },
        ),
    ] = URL(url="https://api.anthropic.com/v1")

    api_type: Annotated[
        Literal["anthropic"],
        Field(title="API Type", description="The type of the API, must be 'anthropic'"),
    ] = "anthropic"

    temperature: Annotated[
        float,
        Field(
            description="The temperature to use for the model, must be between 0 and 2",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Adjust the temperature to change the response style. Lower values lead to more consistent answers, while higher values make the responses more creative. The values must be between 0 and 2."
                }
            },
            ge=0.0,
            le=2.0,
        ),
    ] = 0.8

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> dict[str, Any]:
        my_model: Anthropic = await cls.from_db(model_id)

        api_key_model: AnthropicAPIKey = (
            await my_model.api_key.get_data_model().from_db(my_model.api_key.uuid)
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
