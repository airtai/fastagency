import json
from typing import Any

import jsondiff
import pytest
from pydantic import ValidationError

from fastagency.studio.helpers import create_autogen, get_model_by_ref
from fastagency.studio.models.base import ObjectReference
from fastagency.studio.models.llms.azure import (
    BASE_URL_ERROR_MESSAGE,
    AzureOAI,
    AzureOAIAPIKey,
    UrlModel,
)


def test_import(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AZURE_OAI_API_KEY", raising=False)

    from fastagency.studio.models.llms.azure import AzureOAI

    assert AzureOAI is not None
    assert AzureOAIAPIKey is not None


class TestAzureOAI:
    @pytest.mark.db
    @pytest.mark.asyncio
    async def test_azure_constructor(
        self, azure_oai_gpt35_ref: ObjectReference
    ) -> None:
        # create data
        model = await get_model_by_ref(azure_oai_gpt35_ref)
        assert isinstance(model, AzureOAI)

        # dynamically created data
        name = model.name
        api_key_uuid = model.api_key.uuid  # type: ignore [attr-defined]
        base_url = model.base_url  # type: ignore [attr-defined]
        expected = {
            "name": name,
            "model": "gpt-35-turbo-16k",
            "api_key": {
                "type": "secret",
                "name": "AzureOAIAPIKey",
                "uuid": api_key_uuid,
            },
            "base_url": base_url,
            "api_type": "azure",
            "api_version": "2024-02-01",
            "temperature": 0.0,
        }
        assert model.model_dump() == expected

    @pytest.mark.parametrize(
        "base_url",
        [
            "https://{your-resource-name.openai.azure.com",
            "https://your-resource-name}.openai.azure.com",
            "https://{your-resource-name}.openai.azure.com",
        ],
    )
    @pytest.mark.db
    @pytest.mark.asyncio
    async def test_azure_constructor_with_invalid_base_url(
        self, azure_oai_gpt35_ref: ObjectReference, base_url: str
    ) -> None:
        # create data
        model = await get_model_by_ref(azure_oai_gpt35_ref)
        assert isinstance(model, AzureOAI)

        # Construct a new AzureOAI model with the invalid base_url
        with pytest.raises(ValidationError, match=BASE_URL_ERROR_MESSAGE):
            AzureOAI(
                name=model.name,
                model=model.model,
                api_key=model.api_key,
                base_url=UrlModel(url=base_url).url,
                api_type=model.api_type,
                api_version=model.api_version,
                temperature=model.temperature,
            )

    def test_azure_model_schema(self, pydantic_version: float) -> None:
        schema = AzureOAI.model_json_schema()
        expected = {
            "$defs": {
                "AzureOAIAPIKeyRef": {
                    "properties": {
                        "type": {
                            "const": "secret",
                            "default": "secret",
                            "description": "The name of the type of the data",
                            "enum": ["secret"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "AzureOAIAPIKey",
                            "default": "AzureOAIAPIKey",
                            "description": "The name of the data",
                            "enum": ["AzureOAIAPIKey"],
                            "title": "Name",
                            "type": "string",
                        },
                        "uuid": {
                            "description": "The unique identifier",
                            "format": "uuid",
                            "title": "UUID",
                            "type": "string",
                        },
                    },
                    "required": ["uuid"],
                    "title": "AzureOAIAPIKeyRef",
                    "type": "object",
                }
            },
            "properties": {
                "name": {
                    "description": "The name of the item",
                    "minLength": 1,
                    "title": "Name",
                    "type": "string",
                },
                "model": {
                    "default": "gpt-3.5-turbo",
                    "description": "The model to use for the Azure OpenAI API, e.g. 'gpt-3.5-turbo'",
                    "title": "Model",
                    "type": "string",
                },
                "api_key": {
                    "$ref": "#/$defs/AzureOAIAPIKeyRef",
                    "description": "The API Key from Azure OpenAI",
                    "title": "API Key",
                },
                "base_url": {
                    "default": "https://{your-resource-name}.openai.azure.com",
                    "description": "The base URL of the Azure OpenAI API",
                    "format": "uri",
                    "maxLength": 2083,
                    "minLength": 1,
                    "title": "Base URL",
                    "type": "string",
                },
                "api_type": {
                    "const": "azure",
                    "default": "azure",
                    "description": "The type of the API, must be 'azure'",
                    "enum": ["azure"],
                    "title": "API Type",
                    "type": "string",
                },
                "api_version": {
                    "default": "2024-02-01",
                    "description": "The version of the Azure OpenAI API, e.g. '2024-02-01'",
                    "enum": [
                        "2023-05-15",
                        "2023-06-01-preview",
                        "2023-10-01-preview",
                        "2024-02-15-preview",
                        "2024-03-01-preview",
                        "2024-04-01-preview",
                        "2024-05-01-preview",
                        "2024-02-01",
                    ],
                    "title": "API Version",
                    "type": "string",
                },
                "temperature": {
                    "default": 0.8,
                    "description": "The temperature to use for the model, must be between 0 and 2",
                    "maximum": 2.0,
                    "minimum": 0.0,
                    "title": "Temperature",
                    "type": "number",
                },
            },
            "required": ["name", "api_key"],
            "title": "AzureOAI",
            "type": "object",
        }
        # print(schema)
        pydantic28_delta = '{"properties": {"api_key": {"allOf": [{"$$ref": "#/$defs/AzureOAIAPIKeyRef"}], "$delete": ["$$ref"]}}}'
        if pydantic_version < 2.9:
            # print(f"pydantic28_delta = '{jsondiff.diff(expected, schema, dump=True)}'")
            expected = jsondiff.patch(json.dumps(expected), pydantic28_delta, load=True)
        assert schema == expected

    @pytest.mark.asyncio
    @pytest.mark.db
    async def test_azure_model_create_autogen(
        self,
        user_uuid: str,
        azure_oai_gpt35_ref: ObjectReference,
        azure_gpt35_turbo_16k_llm_config: dict[str, Any],
    ) -> None:
        actual_llm_config = await create_autogen(
            model_ref=azure_oai_gpt35_ref,
            user_uuid=user_uuid,
        )
        assert isinstance(actual_llm_config, dict)
        assert (
            actual_llm_config["config_list"][0]
            == azure_gpt35_turbo_16k_llm_config["config_list"][0]
        )
        assert actual_llm_config == azure_gpt35_turbo_16k_llm_config
