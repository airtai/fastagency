from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field, HttpUrl, field_validator
from pydantic_core import PydanticCustomError
from typing_extensions import TypeAlias

from ..base import Model
from ..registry import register

__all__ = [
    "AzureOAIAPIKey",
    "AzureOAI",
]

AzureApiVersionsLiteral: TypeAlias = Literal[
    "2023-05-15",
    "2023-06-01-preview",
    "2023-10-01-preview",
    "2024-02-15-preview",
    "2024-03-01-preview",
    "2024-04-01-preview",
    "2024-05-01-preview",
    "2024-02-01",
]


@register("secret")
class AzureOAIAPIKey(Model):
    api_key: Annotated[
        str,
        Field(
            title="API Key",
            description="The API Key from Azure OpenAI",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "The API key specified here will be used to authenticate requests to Azure OpenAI services."
                }
            },
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model = await cls.from_db(model_id)

        return my_model.api_key


AzureOAIAPIKeyRef: TypeAlias = AzureOAIAPIKey.get_reference_model()  # type: ignore[valid-type]

# Pydantic adds trailing slash automatically to URLs, so we need to remove it
# https://github.com/pydantic/pydantic/issues/7186#issuecomment-1691594032
URL = Annotated[HttpUrl, AfterValidator(lambda x: str(x).rstrip("/"))]


class UrlModel(BaseModel):
    url: URL


BASE_URL_ERROR_MESSAGE = "The Base URL contains curly braces, indicating a placeholder. Please replace the entire placeholder, including the curly braces, with your actual Azure resource name."


@register("llm")
class AzureOAI(Model):
    model: Annotated[
        str,
        Field(
            description="The model to use for the Azure OpenAI API, e.g. 'gpt-3.5-turbo'",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "The model that the LLM uses to interact with Azure OpenAI services."
                }
            },
        ),
    ] = "gpt-3.5-turbo"

    api_key: Annotated[
        AzureOAIAPIKeyRef,
        Field(
            title="API Key",
            description="The API Key from Azure OpenAI",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Choose the API key that will be used to authenticate requests to Azure OpenAI services."
                }
            },
        ),
    ]

    base_url: Annotated[
        URL,
        Field(
            title="Base URL",
            description="The base URL of the Azure OpenAI API",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "The base URL that the LLM uses to interact with Azure OpenAI services."
                }
            },
        ),
    ] = UrlModel(url="https://{your-resource-name}.openai.azure.com").url

    api_type: Annotated[
        Literal["azure"],
        Field(title="API Type", description="The type of the API, must be 'azure'"),
    ] = "azure"

    api_version: Annotated[
        AzureApiVersionsLiteral,
        Field(
            title="API Version",
            description="The version of the Azure OpenAI API, e.g. '2024-02-01'",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "The version of the Azure OpenAI API that the LLM uses to interact with Azure OpenAI services."
                }
            },
        ),
    ] = "2024-02-01"

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

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls: type["AzureOAI"], value: Any) -> Any:
        if "{" in value or "}" in value:
            raise PydanticCustomError("invalid_base_url", BASE_URL_ERROR_MESSAGE)
        return value

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> dict[str, Any]:
        my_model = await cls.from_db(model_id)

        api_key_model = await my_model.api_key.get_data_model().from_db(
            my_model.api_key.uuid
        )
        api_key = await api_key_model.create_autogen(my_model.api_key.uuid, user_id)

        config_list = [
            {
                "model": my_model.model,
                "api_key": api_key,
                "base_url": str(my_model.base_url),
                "api_type": my_model.api_type,
                "api_version": my_model.api_version,
            }
        ]

        llm_config = {
            "config_list": config_list,
            "temperature": my_model.temperature,
        }

        return llm_config
