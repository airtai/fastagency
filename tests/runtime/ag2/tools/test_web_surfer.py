from typing import Any

import pytest
from autogen import ConversableAgent, UserProxyAgent

from fastagency.runtimes.ag2.ag2 import Toolable
from fastagency.runtimes.ag2.tools import WebSurferTool


class TestWebSurferTool:
    def test_web_surfer_chat_constructor_positive(
        self, azure_gpt4o_llm_config: dict[str, Any]
    ) -> None:
        web_surfer_tool = WebSurferTool(
            name_prefix="test",
            llm_config=azure_gpt4o_llm_config,
            summarizer_llm_config=azure_gpt4o_llm_config,
        )
        assert isinstance(web_surfer_tool, Toolable)

    def test_web_surfer_chat_constructor_with_invalid_llm_config(
        self,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="When using OpenAI or Azure OpenAI endpoints, specify a non-empty 'model' either in 'llm_config' or in each config of 'config_list'.",
        ):
            WebSurferTool(
                name_prefix="test",
                llm_config={},
                summarizer_llm_config={},
            )

    @pytest.mark.llm
    def test_web_surfer_chat_register(
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

        web_surfer = WebSurferTool(
            name_prefix="Web_Surfer",
            llm_config=azure_gpt4o_llm_config,
            summarizer_llm_config=azure_gpt4o_llm_config,
        )

        web_surfer.register(
            caller=assistant_agent,
            executor=user_agent,
        )

    @pytest.mark.parametrize(
        ("task", "answer"),
        [
            (
                "Visit https://en.wikipedia.org/wiki/Zagreb and tell me when Zagreb became a free royal city.",
                "1242",
            ),
            # "What is the most expensive NVIDIA GPU on https://www.alternate.de/ and how much it costs?",
            # "Compile a list of news headlines under section 'Politika i kriminal' on telegram.hr.",
            # "What is the single the most newsworthy story today?",
            # "Given that weather forecast today is warm and sunny, what would be the best way to spend an evening in Zagreb according to the weather forecast?",
        ],
    )
    @pytest.mark.openai
    @pytest.mark.xfail(strict=False)
    def test_web_surfer_chat_simple_task(
        self, openai_gpt4o_mini_llm_config: dict[str, Any], task: str, answer: str
    ) -> None:
        user_agent = UserProxyAgent(
            name="User_Agent",
            system_message="You are a user agent",
            llm_config=openai_gpt4o_mini_llm_config,
            human_input_mode="NEVER",
        )
        assistant_agent = ConversableAgent(
            name="Assistant_Agent",
            system_message="You are a useful assistant",
            llm_config=openai_gpt4o_mini_llm_config,
            human_input_mode="NEVER",
        )

        web_surfer = WebSurferTool(
            name_prefix="Web_Surfer",
            llm_config=openai_gpt4o_mini_llm_config,
            summarizer_llm_config=openai_gpt4o_mini_llm_config,
        )

        web_surfer.register(
            caller=assistant_agent,
            executor=user_agent,
        )

        chat_result = user_agent.initiate_chat(
            assistant_agent,
            message=task,
            summary_method="reflection_with_llm",
            max_turns=3,
        )

        assert answer in chat_result.summary.lower()

        xs = [
            m["content"] if m["content"] is not None else ""
            for m in chat_result.chat_history
            if m is not None
        ]
        assert any("We have successfully completed the task" in m for m in xs)
