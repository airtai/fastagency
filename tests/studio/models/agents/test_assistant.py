from typing import Any

import autogen
import pytest

from fastagency.api.openapi import OpenAPI
from fastagency.studio.helpers import create_autogen
from fastagency.studio.models.agents.assistant import AssistantAgent
from fastagency.studio.models.base import ObjectReference

from ....helpers import get_by_tag, parametrize_fixtures


class TestAssistantAgent:
    @pytest.mark.asyncio
    @pytest.mark.db
    @pytest.mark.llm
    @parametrize_fixtures("assistant_ref", get_by_tag("assistant"))
    async def test_assistant_construction(
        self,
        user_uuid: str,
        assistant_ref: ObjectReference,
    ) -> None:
        print(f"test_assistant_construction({user_uuid=}, {assistant_ref=})")  # noqa: T201

    def test_assistant_model_schema(self) -> None:
        schema = AssistantAgent.model_json_schema()
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
                "system_message": {
                    "default": "You are a helpful assistant. After you successfully answer all questions and there are no new questions asked after your response (e.g. there is no specific direction or question asked after you give a response), terminate the chat by outputting 'TERMINATE' (IMPORTANT: use all caps)",
                    "description": "The system message of the agent. This message is used to inform the agent about his role in the conversation",
                    "title": "System Message",
                    "type": "string",
                },
            },
            "required": ["name", "llm"],
            "title": "AssistantAgent",
            "type": "object",
        }
        # print(f"{schema=}")
        assert schema == expected

    @pytest.mark.asyncio
    @pytest.mark.db
    @parametrize_fixtures("assistant_ref", get_by_tag("assistant", "weather"))
    async def test_assistant_create_autogen(
        self,
        user_uuid: str,
        assistant_ref: ObjectReference,
    ) -> None:
        def is_termination_msg(msg: dict[str, Any]) -> bool:
            return "TERMINATE" in ["content"]

        ag_assistant, ag_toolkits = await create_autogen(
            model_ref=assistant_ref,
            user_uuid=user_uuid,
            is_termination_msg=is_termination_msg,
        )
        assert isinstance(ag_assistant, autogen.agentchat.AssistantAgent)
        assert isinstance(ag_toolkits[0], OpenAPI)
        assert len(ag_toolkits) == 1
        assert ag_assistant._is_termination_msg == is_termination_msg

    @pytest.mark.asyncio
    @pytest.mark.db
    @pytest.mark.llm
    @parametrize_fixtures("assistant_ref", get_by_tag("assistant", "weather"))
    async def test_assistant_weather_end2end(
        self,
        user_uuid: str,
        assistant_ref: ObjectReference,
    ) -> None:
        ag_assistant, ag_toolkits = await create_autogen(
            model_ref=assistant_ref,
            user_uuid=user_uuid,
        )

        user_proxy = autogen.agentchat.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
        )
        weather_tool: OpenAPI = ag_toolkits[0]
        weather_tool.register_for_execution(user_proxy)
        weather_tool.register_for_llm(ag_assistant)
        chat_result = user_proxy.initiate_chat(
            ag_assistant, message="What is the weather in New York?"
        )

        messages = [msg["content"] for msg in chat_result.chat_history]
        for w in ["New York", "sunny", "TERMINATE"]:
            assert any(msg is not None and w in msg for msg in messages), (w, messages)
