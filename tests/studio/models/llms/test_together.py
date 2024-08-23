import uuid
from typing import Dict

import pytest
from together import Together

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
        client = Together()

        expected_together_model_string: Dict[str, str] = {
            model.display_name: model.id
            for model in client.models.list()
            if model.type == "chat"
        }

        # print(expected_together_model_string)
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
                    "default": "Meta Llama 3 70B Reference",
                    "description": "The model to use for the Together API",
                    "enum": [
                        "WizardLM v1.2 (13B)",
                        "Code Llama Instruct (34B)",
                        "Upstage SOLAR Instruct v1 (11B)",
                        "Meta Llama 3 70B Reference",
                        "OpenHermes-2-Mistral (7B)",
                        "LLaMA-2-7B-32K-Instruct (7B)",
                        "ReMM SLERP L2 (13B)",
                        "Toppy M (7B)",
                        "OpenChat 3.5",
                        "Chronos Hermes (13B)",
                        "Snorkel Mistral PairRM DPO (7B)",
                        "Qwen 1.5 Chat (7B)",
                        "Qwen 1.5 Chat (14B)",
                        "Qwen 1.5 Chat (1.8B)",
                        "Snowflake Arctic Instruct",
                        "Nous Hermes 2 - Mixtral 8x7B-SFT",
                        "Nous Hermes 2 - Mixtral 8x7B-DPO ",
                        "Deepseek Coder Instruct (33B)",
                        "Nous Hermes Llama-2 (13B)",
                        "Vicuna v1.5 (13B)",
                        "Qwen 1.5 Chat (0.5B)",
                        "Code Llama Instruct (7B)",
                        "Nous Hermes-2 Yi (34B)",
                        "Code Llama Instruct (13B)",
                        "Llama3 8B Chat HF INT4",
                        "OpenHermes-2.5-Mistral (7B)",
                        "Nous Capybara v1.9 (7B)",
                        "Meta Llama 3.1 70B Instruct Turbo",
                        "Nous Hermes 2 - Mistral DPO (7B)",
                        "StripedHyena Nous (7B)",
                        "Alpaca (7B)",
                        "Platypus2 Instruct (70B)",
                        "Gemma Instruct (2B)",
                        "Gemma Instruct (7B)",
                        "LLaMA-2 Chat (7B)",
                        "OLMo Instruct (7B)",
                        "Qwen 1.5 Chat (4B)",
                        "MythoMax-L2 (13B)",
                        "Mistral (7B) Instruct",
                        "Mistral (7B) Instruct v0.2",
                        "Meta Llama 3.1 8B Instruct Turbo",
                        "OpenOrca Mistral (7B) 8K",
                        "Nous Hermes LLaMA-2 (7B)",
                        "Qwen 1.5 Chat (32B)",
                        "Qwen 2 Instruct (72B)",
                        "Qwen 1.5 Chat (72B)",
                        "DeepSeek LLM Chat (67B)",
                        "Vicuna v1.5 (7B)",
                        "WizardLM-2 (8x22B)",
                        "Togethercomputer Llama3 8B Instruct Int8",
                        "Mistral (7B) Instruct v0.3",
                        "Qwen 1.5 Chat (110B)",
                        "LLaMA-2 Chat (13B)",
                        "Gemma-2 Instruct (27B)",
                        "01-ai Yi Chat (34B)",
                        "Meta Llama 3 70B Instruct Turbo",
                        "Meta Llama 3 70B Instruct Lite",
                        "Gemma-2 Instruct (9B)",
                        "Meta Llama 3 8B Reference",
                        "Mixtral-8x7B Instruct v0.1",
                        "Code Llama Instruct (70B)",
                        "Meta Llama 3.1 405B Instruct Turbo",
                        "DBRX Instruct",
                        "Meta Llama 3.1 8B Instruct",
                        "Meta Llama 3 8B Instruct Turbo",
                        "Dolphin 2.5 Mixtral 8x7b",
                        "Mixtral-8x22B Instruct v0.1",
                        "Meta Llama 3 8B Instruct Lite",
                        "LLaMA-2 Chat (70B)",
                        "Koala (7B)",
                        "Qwen 2 Instruct (1.5B)",
                        "Qwen 2 Instruct (7B)",
                        "Guanaco (65B) ",
                        "Vicuna v1.3 (7B)",
                        "Nous Hermes LLaMA-2 (70B)",
                        "Vicuna v1.5 16K (13B)",
                        "Zephyr-7B-ß",
                        "Guanaco (13B) ",
                        "Vicuna v1.3 (13B)",
                        "Guanaco (33B) ",
                        "Koala (13B)",
                        "Upstage SOLAR Instruct v1 (11B)-Int4",
                        "Guanaco (7B) ",
                        "Meta Llama 3 8B Instruct",
                        "Meta Llama 3 70B Instruct",
                        "Hermes 2 Theta Llama-3 70B",
                        "carson ml318bit",
                        "carson ml31405bit",
                        "carson ml3170bit",
                        "carson ml318br",
                        "Llama-3 70B Instruct Gradient 1048K",
                        "Meta Llama 3.1 70B Instruct",
                        "Meta Llama 3.1 70B",
                    ],
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
                    "title": "Base Url",
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
        assert "Meta Llama 3 70B Reference" in schema["properties"]["model"]["enum"]
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
