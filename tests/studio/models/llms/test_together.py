import uuid
from typing import Dict

import pytest
import together

from fastagency.studio.helpers import get_model_by_ref
from fastagency.studio.models.base import ObjectReference
from fastagency.studio.models.llms.together import (
    TogetherAI,
    TogetherAIAPIKey,
    together_model_string,
)


def test_import(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TOGETHER_API_KEY", raising=False)

    from fastagency.studio.models.llms.together import TogetherAI, TogetherAIAPIKey

    assert TogetherAI is not None
    assert TogetherAIAPIKey is not None


class TestTogetherAIAPIKey:
    def test_constructor_success(self) -> None:
        api_key = TogetherAIAPIKey(
            api_key="*" * 64,  # pragma: allowlist secret
            name="Hello World!",
        )  # pragma: allowlist secret
        assert (
            api_key.api_key == "*" * 64  # pragma: allowlist secret
        )  # pragma: allowlist secret

    def test_constructor_failure(self) -> None:
        with pytest.raises(
            ValueError, match="String should have at least 64 characters"
        ):
            TogetherAIAPIKey(
                api_key="not a proper key",  # pragma: allowlist secret
                name="Hello World!",
            )  # pragma: allowlist secret


class TestTogetherAI:
    @pytest.mark.togetherai
    def test_together_model_string(self) -> None:
        # requires that environment variables TOGETHER_API_KEY is set
        client = together.Together()

        expected_together_model_string: Dict[str, str] = {
            model.display_name: model.id
            for model in client.models.list()
            if model.type == "chat"
        }

        print(expected_together_model_string)
        assert together_model_string == expected_together_model_string

    @pytest.mark.db
    @pytest.mark.asyncio
    async def test_togetherai_constructor(
        self,
        togetherai_ref: ObjectReference,
    ) -> None:
        # create data
        model = await get_model_by_ref(togetherai_ref)
        assert isinstance(model, TogetherAI)

        # dynamically created data
        name = model.name
        api_key_uuid = model.api_key.uuid  # type: ignore [attr-defined]

        expected = {
            "name": name,
            "model": "Mixtral-8x7B Instruct v0.1",
            "api_key": {
                "type": "secret",
                "name": "TogetherAIAPIKey",
                "uuid": api_key_uuid,
            },
            "base_url": "https://api.together.xyz/v1",
            "api_type": "togetherai",
            "temperature": 0.8,
        }
        assert model.model_dump() == expected

    def test_togetherai_schema(self) -> None:
        schema = TogetherAI.model_json_schema()
        expected = {
            "$defs": {
                "TogetherAIAPIKeyRef": {
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
                            "const": "TogetherAIAPIKey",
                            "default": "TogetherAIAPIKey",
                            "description": "The name of the data",
                            "enum": ["TogetherAIAPIKey"],
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
                    "title": "TogetherAIAPIKeyRef",
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
                    "default": "Meta Llama 3 70B Instruct Reference",
                    "description": "The model to use for the Together API",
                    "title": "Model",
                    "type": "string",
                },
                "api_key": {
                    "allOf": [{"$ref": "#/$defs/TogetherAIAPIKeyRef"}],
                    "description": "The API Key from Together.ai",
                    "title": "API Key",
                },
                "base_url": {
                    "default": "https://api.together.xyz/v1",
                    "description": "The base URL of the OpenAI API",
                    "format": "uri",
                    "maxLength": 2083,
                    "minLength": 1,
                    "title": "Base URL",
                    "type": "string",
                },
                "api_type": {
                    "const": "togetherai",
                    "default": "togetherai",
                    "description": "The type of the API, must be 'togetherai'",
                    "enum": ["togetherai"],
                    "title": "API Type",
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
            "title": "TogetherAI",
            "type": "object",
        }
        assert (
            "Meta Llama 3 70B Instruct Reference"
            in schema["properties"]["model"]["enum"]
        )
        schema["properties"]["model"].pop("enum")
        assert schema == expected

    @pytest.mark.asyncio
    @pytest.mark.db
    async def test_togetherai_model_create_autogen(
        self,
        user_uuid: str,
        togetherai_ref: ObjectReference,
    ) -> None:
        actual_llm_config = await TogetherAI.create_autogen(
            model_id=togetherai_ref.uuid,
            user_id=uuid.UUID(user_uuid),
        )
        assert isinstance(actual_llm_config, dict)
        api_key = actual_llm_config["config_list"][0]["api_key"]
        expected = {
            "config_list": [
                {
                    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                    "api_key": api_key,
                    "base_url": "https://api.together.xyz/v1",
                    "api_type": "togetherai",
                }
            ],
            "temperature": 0.8,
        }

        assert actual_llm_config == expected
