import uuid

import pytest

from fastagency.helpers import get_model_by_ref
from fastagency.models.base import ObjectReference
from fastagency.models.llms.anthropic import Anthropic, AnthropicAPIKey


def test_import(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    from fastagency.models.llms.anthropic import Anthropic

    assert Anthropic is not None
    assert AnthropicAPIKey is not None


class TestAnthropic:
    @pytest.mark.db()
    @pytest.mark.asyncio()
    async def test_anthropic_constructor(self, anthropic_ref: ObjectReference) -> None:
        # create data
        model = await get_model_by_ref(anthropic_ref)
        assert isinstance(model, Anthropic)

        # dynamically created data
        name = model.name
        api_key_uuid = model.api_key.uuid  # type: ignore [attr-defined]

        expected = {
            "name": name,
            "model": "claude-3-5-sonnet-20240620",
            "api_key": {
                "type": "secret",
                "name": "AnthropicAPIKey",
                "uuid": api_key_uuid,
            },
            "base_url": "https://api.anthropic.com/v1",
            "api_type": "anthropic",
            "temperature": 0.8,
        }
        assert model.model_dump() == expected

    def test_anthropic_constructor_failure(self) -> None:
        with pytest.raises(ValueError, match="Invalid Anthropic API Key"):
            AnthropicAPIKey(
                api_key="_sk-sUeBP9asw6GiYHXqtg70T3BlbkFJJuLwJFco90bOpU0Ntest",  # pragma: allowlist secret
                name="Hello World!",
            )

    def test_anthropic_model_schema(self) -> None:
        schema = Anthropic.model_json_schema()
        expected = {
            "$defs": {
                "AnthropicAPIKeyRef": {
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
                            "const": "AnthropicAPIKey",
                            "default": "AnthropicAPIKey",
                            "description": "The name of the data",
                            "enum": ["AnthropicAPIKey"],
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
                    "title": "AnthropicAPIKeyRef",
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
                    "default": "claude-3-5-sonnet-20240620",
                    "description": "The model to use for the Anthropic API, e.g. 'claude-3-5-sonnet-20240620'",
                    "enum": [
                        "claude-3-5-sonnet-20240620",
                        "claude-3-opus-20240229",
                        "claude-3-sonnet-20240229",
                        "claude-3-haiku-20240307",
                    ],
                    "title": "Model",
                    "type": "string",
                },
                "api_key": {"$ref": "#/$defs/AnthropicAPIKeyRef"},
                "base_url": {
                    "default": "https://api.anthropic.com/v1",
                    "description": "The base URL of the Anthropic API",
                    "format": "uri",
                    "maxLength": 2083,
                    "minLength": 1,
                    "title": "Base Url",
                    "type": "string",
                },
                "api_type": {
                    "const": "anthropic",
                    "default": "anthropic",
                    "description": "The type of the API, must be 'anthropic'",
                    "enum": ["anthropic"],
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
            "title": "Anthropic",
            "type": "object",
        }
        assert schema == expected

    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.anthropic()
    async def test_anthropic_model_create_autogen(
        self,
        user_uuid: str,
        anthropic_ref: ObjectReference,
    ) -> None:
        actual_llm_config = await Anthropic.create_autogen(
            model_id=anthropic_ref.uuid,
            user_id=uuid.UUID(user_uuid),
        )
        assert isinstance(actual_llm_config, dict)
        api_key = actual_llm_config["config_list"][0]["api_key"]
        expected = {
            "config_list": [
                {
                    "model": "claude-3-5-sonnet-20240620",
                    "api_key": api_key,
                    "base_url": "https://api.anthropic.com/v1",
                    "api_type": "anthropic",
                }
            ],
            "temperature": 0.8,
        }

        assert actual_llm_config == expected
