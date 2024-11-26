from typing import Any

import pytest
from autogen import ConversableAgent, UserProxyAgent

from fastagency.runtimes.ag2.agents.whatsapp import WhatsAppAgent
from fastagency.runtimes.ag2.autogen import Toolable
from fastagency.runtimes.ag2.tools import WhatsAppTool


class TestWhatsApp:
    def test_whatsapp_chat_constructor_positive(self) -> None:
        whatsapp_tool = WhatsAppTool(
            whatsapp_api_key="api_key",  # pragma: allowlist secret
        )
        assert isinstance(whatsapp_tool, Toolable)

    @pytest.mark.llm
    def test_whatsapp_chat_register(
        self, azure_gpt4o_llm_config: dict[str, Any]
    ) -> None:
        user_agent = UserProxyAgent(
            name="User_Agent",
            system_message="You are a user agent",
            llm_config=azure_gpt4o_llm_config,
            human_input_mode="NEVER",
        )
        assistant_agent = ConversableAgent(
            name="Assistant_Agent",
            system_message="You are a useful assistant",
            llm_config=azure_gpt4o_llm_config,
            human_input_mode="NEVER",
        )

        whatsapp_tool = WhatsAppTool(
            whatsapp_api_key="api_key",  # pragma: allowlist secret
        )

        whatsapp_tool.register(
            caller=assistant_agent,
            executor=user_agent,
        )

        registered_function = assistant_agent.llm_config["tools"][0]["function"]
        assert registered_function["name"] == "send_whatsapp_text_message"

    @pytest.mark.llm
    def test_whatsapp_agent(self, azure_gpt4o_llm_config: dict[str, Any]) -> None:
        user_agent = UserProxyAgent(
            name="User_Agent",
            system_message="You are a user agent",
            llm_config=azure_gpt4o_llm_config,
            human_input_mode="NEVER",
        )
        assistant_agent = WhatsAppAgent(
            name="Whatsapp_Agent",
            llm_config=azure_gpt4o_llm_config,
            human_input_mode="NEVER",
            executor=user_agent,
            sender="447860099299",
            whatsapp_api_key="api_key",  # pragma: allowlist secret
        )

        registered_function = assistant_agent.llm_config["tools"][0]["function"]
        assert registered_function["name"] == "send_whatsapp_text_message"
