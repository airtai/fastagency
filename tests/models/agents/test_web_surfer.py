import uuid
from typing import Any, Dict

import autogen.agentchat.contrib.web_surfer
import pytest
from fastapi import BackgroundTasks

from fastagency.app import add_model
from fastagency.helpers import create_autogen
from fastagency.models.agents.web_surfer import BingAPIKey, WebSurferAgent
from fastagency.models.base import ObjectReference
from fastagency.models.llms.azure import AzureOAIAPIKey
from tests.helpers import get_by_tag, parametrize_fixtures


class TestWebSurferAgent:
    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.llm()
    @parametrize_fixtures("websurfer_ref", get_by_tag("websurfer"))
    async def test_websurfer_construction(
        self,
        user_uuid: str,
        websurfer_ref: ObjectReference,
    ) -> None:
        print(f"test_websurfer_construction({user_uuid=}, {websurfer_ref=})")  # noqa: T201

    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.llm()
    @parametrize_fixtures("llm_ref", get_by_tag("websurfer-llm"))
    async def test_websurfer_llm_construction(
        self,
        user_uuid: str,
        llm_ref: ObjectReference,
    ) -> None:
        print(f"test_websurfer_llm_construction({user_uuid=}, {llm_ref=})")  # noqa: T201

    def test_web_surfer_model_schema(self) -> None:
        schema = WebSurferAgent.model_json_schema()
        expected = {
            "$defs": {
                "AnthropicRef": {
                    "properties": {
                        "type": {
                            "const": "llm",
                            "default": "llm",
                            "description": "The name of the type of the data",
                            "enum": ["llm"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "Anthropic",
                            "default": "Anthropic",
                            "description": "The name of the data",
                            "enum": ["Anthropic"],
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
                    "title": "AnthropicRef",
                    "type": "object",
                },
                "AzureOAIRef": {
                    "properties": {
                        "type": {
                            "const": "llm",
                            "default": "llm",
                            "description": "The name of the type of the data",
                            "enum": ["llm"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "AzureOAI",
                            "default": "AzureOAI",
                            "description": "The name of the data",
                            "enum": ["AzureOAI"],
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
                    "title": "AzureOAIRef",
                    "type": "object",
                },
                "BingAPIKeyRef": {
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
                            "const": "BingAPIKey",
                            "default": "BingAPIKey",
                            "description": "The name of the data",
                            "enum": ["BingAPIKey"],
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
                    "title": "BingAPIKeyRef",
                    "type": "object",
                },
                "OpenAIRef": {
                    "properties": {
                        "type": {
                            "const": "llm",
                            "default": "llm",
                            "description": "The name of the type of the data",
                            "enum": ["llm"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "OpenAI",
                            "default": "OpenAI",
                            "description": "The name of the data",
                            "enum": ["OpenAI"],
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
                    "title": "OpenAIRef",
                    "type": "object",
                },
                "TogetherAIRef": {
                    "properties": {
                        "type": {
                            "const": "llm",
                            "default": "llm",
                            "description": "The name of the type of the data",
                            "enum": ["llm"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "TogetherAI",
                            "default": "TogetherAI",
                            "description": "The name of the data",
                            "enum": ["TogetherAI"],
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
                    "title": "TogetherAIRef",
                    "type": "object",
                },
                "ToolboxRef": {
                    "properties": {
                        "type": {
                            "const": "toolbox",
                            "default": "toolbox",
                            "description": "The name of the type of the data",
                            "enum": ["toolbox"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "Toolbox",
                            "default": "Toolbox",
                            "description": "The name of the data",
                            "enum": ["Toolbox"],
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
                    "title": "ToolboxRef",
                    "type": "object",
                },
            },
            "properties": {
                "name": {
                    "description": "The name of the item",
                    "minLength": 1,
                    "title": "Name",
                    "type": "string",
                },
                "llm": {
                    "anyOf": [
                        {"$ref": "#/$defs/AnthropicRef"},
                        {"$ref": "#/$defs/AzureOAIRef"},
                        {"$ref": "#/$defs/OpenAIRef"},
                        {"$ref": "#/$defs/TogetherAIRef"},
                    ],
                    "description": "LLM used by the agent for producing responses",
                    "title": "LLM",
                },
                "toolbox_1": {
                    "anyOf": [{"$ref": "#/$defs/ToolboxRef"}, {"type": "null"}],
                    "default": None,
                    "description": "Toolbox used by the agent for producing responses",
                    "title": "Toolbox",
                },
                "toolbox_2": {
                    "anyOf": [{"$ref": "#/$defs/ToolboxRef"}, {"type": "null"}],
                    "default": None,
                    "description": "Toolbox used by the agent for producing responses",
                    "title": "Toolbox",
                },
                "toolbox_3": {
                    "anyOf": [{"$ref": "#/$defs/ToolboxRef"}, {"type": "null"}],
                    "default": None,
                    "description": "Toolbox used by the agent for producing responses",
                    "title": "Toolbox",
                },
                "summarizer_llm": {
                    "anyOf": [
                        {"$ref": "#/$defs/AnthropicRef"},
                        {"$ref": "#/$defs/AzureOAIRef"},
                        {"$ref": "#/$defs/OpenAIRef"},
                        {"$ref": "#/$defs/TogetherAIRef"},
                    ],
                    "description": "This LLM will be used to generated summary of all pages visited",
                    "title": "Summarizer LLM",
                },
                "viewport_size": {
                    "default": 1080,
                    "description": "The viewport size of the browser",
                    "title": "Viewport Size",
                    "type": "integer",
                },
                "bing_api_key": {
                    "anyOf": [{"$ref": "#/$defs/BingAPIKeyRef"}, {"type": "null"}],
                    "default": None,
                    "description": "The Bing API key for the browser",
                },
            },
            "required": ["name", "llm", "summarizer_llm"],
            "title": "WebSurferAgent",
            "type": "object",
        }
        assert schema == expected

    @pytest.mark.asyncio()
    @pytest.mark.db()
    @parametrize_fixtures("websurfer_ref", get_by_tag("websurfer"))
    async def test_assistant_create_autogen(
        self,
        user_uuid: str,
        websurfer_ref: ObjectReference,
    ) -> None:
        def is_termination_msg(msg: Dict[str, Any]) -> bool:
            return "TERMINATE" in ["content"]

        ag_assistant, ag_toolkits = await create_autogen(
            model_ref=websurfer_ref,
            user_uuid=user_uuid,
            is_termination_msg=is_termination_msg,
        )
        assert isinstance(
            ag_assistant, autogen.agentchat.contrib.web_surfer.WebSurferAgent
        )
        assert len(ag_toolkits) == 0

    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.llm()
    @parametrize_fixtures("websurfer_ref", get_by_tag("websurfer"))
    async def test_websurfer_end2end(
        self,
        user_uuid: str,
        websurfer_ref: ObjectReference,
        assistant_noapi_openai_oai_gpt35_ref: ObjectReference,
    ) -> None:
        ag_websurfer, _ = await create_autogen(
            model_ref=websurfer_ref,
            user_uuid=user_uuid,
        )

        ag_user_proxy = autogen.agentchat.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
        )

        chat_result = ag_user_proxy.initiate_chat(
            ag_websurfer,
            message="Visit https://en.wikipedia.org/wiki/Zagreb and tell me when Zagreb became a free royal city.",
        )

        messages = [msg["content"] for msg in chat_result.chat_history]
        assert messages
        for w in ["1242", "Zagreb", "free royal city"]:
            assert any(msg is not None and w in msg for msg in messages), (w, messages)

    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.llm()
    @parametrize_fixtures("websurfer_ref", get_by_tag("websurfer"))
    async def test_websurfer_and_toolkit_end2end(
        self,
        user_uuid: str,
        websurfer_ref: ObjectReference,
        assistant_weather_openai_oai_gpt35_ref: ObjectReference,
        openai_gpt35_turbo_16k_llm_config: Dict[str, Any],
    ) -> None:
        ag_websurfer, _ = await create_autogen(
            model_ref=websurfer_ref,
            user_uuid=user_uuid,
        )

        ag_assistant, ag_toolboxes = await create_autogen(
            model_ref=assistant_weather_openai_oai_gpt35_ref,
            user_uuid=user_uuid,
        )

        ag_user_proxy = autogen.agentchat.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=4,
        )

        ag_toolbox = ag_toolboxes[0]
        ag_toolbox.register_for_llm(ag_assistant)
        ag_toolbox.register_for_execution(ag_user_proxy)

        groupchat = autogen.GroupChat(
            agents=[ag_assistant, ag_websurfer, ag_user_proxy],
            messages=[],
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=openai_gpt35_turbo_16k_llm_config,
        )
        chat_result = manager.initiate_chat(
            recipient=manager,
            message="Find out what's the weather in Zagreb today and then visit https://www.infozagreb.hr/hr/dogadanja and check what would be the best way to spend an evening in Zagreb according to the weather forecast.",
        )

        messages = [msg["content"] for msg in chat_result.chat_history]
        assert messages

        # print("*" * 80)
        # print()
        # for msg in messages:
        #     print(msg)
        #     print()
        # print("*" * 80)

        # for w in ["sunny", "Zagreb", ]:
        #     assert any(msg is not None and w in msg for msg in messages), (w, messages)


# todo
class TestBingAPIKey:
    @pytest.mark.asyncio()
    @pytest.mark.db()
    async def test_bing_api_key_model_create_autogen(
        self,
        azure_gpt35_turbo_16k_llm_config: Dict[str, Any],
        user_uuid: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # Add secret to database
        api_key = BingAPIKey(  # type: ignore [operator]
            api_key="dummy_bing_api_key",  # pragma: allowlist secret
            name="api_key_model_name",
        )
        api_key_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="secret",
            model_name=BingAPIKey.__name__,  # type: ignore [attr-defined]
            model_uuid=api_key_model_uuid,
            model=api_key.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        # Call create_autogen
        actual_api_key = await AzureOAIAPIKey.create_autogen(
            model_id=uuid.UUID(api_key_model_uuid),
            user_id=uuid.UUID(user_uuid),
        )
        assert isinstance(actual_api_key, str)
        assert actual_api_key == api_key.api_key
