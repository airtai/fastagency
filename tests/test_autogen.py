from typing import Annotated, Any

import pytest
from autogen.agentchat import ConversableAgent, UserProxyAgent

from fastagency import Chatable, IOMessage
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.runtimes.autogen.base import _findall, _match
from fastagency.ui.console import ConsoleUI
from tests.conftest import InputMock


class TestPatternMatching:
    def test_end_of_message(self) -> None:
        chunk = "\n--------------------------------------------------------------------------------\n"
        assert _match("end_of_message", chunk)

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[31m\n>>>>>>>> USING AUTO REPLY...\x1b[0m\n",
            "\n>>>>>>>> USING AUTO REPLY...\n",
        ],
    )
    def test_auto_reply(self, chunk: str) -> None:
        assert _match("auto_reply", chunk)

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[33mUser_Proxy\x1b[0m (to Weatherman):\n\n",
            "User_Proxy (to Weatherman):\n\n",
        ],
    )
    def test_sender_recipient(self, chunk: str) -> None:
        assert _match("sender_recipient", chunk)
        sender, recipient = _findall("sender_recipient", chunk)

        assert sender == "User_Proxy"
        assert recipient == "Weatherman"

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[32m***** Suggested tool call (call_HNs2kuTywlvatTY5WHzMLfDL): get_daily_weather_daily_get *****\x1b[0m\n",
            "***** Suggested tool call (call_HNs2kuTywlvatTY5WHzMLfDL): get_daily_weather_daily_get *****\n",
        ],
    )
    def test_suggested_function_call(self, chunk: str) -> None:
        assert _match("suggested_function_call", chunk)

        call_id, function_name = _findall("suggested_function_call", chunk)

        assert call_id == "call_HNs2kuTywlvatTY5WHzMLfDL"
        assert function_name == "get_daily_weather_daily_get"

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[32m**********************************************************************************************\x1b[0m\n",
            "**********************************************************************************************\n",
        ],
    )
    def test_stars(self, chunk: str) -> None:
        assert _match("stars", chunk)

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[35m\n>>>>>>>> EXECUTING FUNCTION get_daily_weather_daily_get...\x1b[0m\n",
            "\n>>>>>>>> EXECUTING FUNCTION get_daily_weather_daily_get...\n",
        ],
    )
    def test_function_call_execution(self, chunk: str) -> None:
        assert _match("function_call_execution", chunk)

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[32m***** Response from calling tool (call_HNs2kuTywlvatTY5WHzMLfDL) *****\x1b[0m\n",
            "***** Response from calling tool (call_HNs2kuTywlvatTY5WHzMLfDL) *****\n",
        ],
    )
    def test_response_from_calling_tool(self, chunk: str) -> None:
        assert _match("response_from_calling_tool", chunk)

        call_id = _findall("response_from_calling_tool", chunk)
        assert call_id == "call_HNs2kuTywlvatTY5WHzMLfDL"  # type: ignore[comparison-overlap]

    @pytest.mark.parametrize(
        "chunk",
        [
            "\x1b[31m\n>>>>>>>> NO HUMAN INPUT RECEIVED.\x1b[0m",
            "\n>>>>>>>> NO HUMAN INPUT RECEIVED.",
        ],
    )
    def test_no_human_input_received(self, chunk: str) -> None:
        assert _match("no_human_input_received", chunk)

    def test_user_interrupted(self) -> None:
        chunk = "USER INTERRUPTED\n"
        assert _match("user_interrupted", chunk)

    def test_arguments(self) -> None:
        chunk = 'Arguments: \n{"city": "Zagreb"}\n'
        assert _match("arguments", chunk)

        arguments = _findall("arguments", chunk)

        assert arguments == '{"city": "Zagreb"}'  # type: ignore[comparison-overlap]

    def test_auto_reply_input(self) -> None:
        prompt = "Replying as User_Proxy. Provide feedback to Weatherman. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: "

        assert _match("auto_reply_input", prompt)

        sender, recipient = _findall("auto_reply_input", prompt)
        assert sender == "User_Proxy"
        assert recipient == "Weatherman"


@pytest.mark.openai
def test_simple(openai_gpt4o_mini_llm_config: dict[str, Any]) -> None:
    wf = AutoGenWorkflows()

    @wf.register(
        name="simple_learning", description="Student and teacher learning chat"
    )
    def simple_workflow(io: Chatable, initial_message: str, session_id: str) -> str:
        student_agent = ConversableAgent(
            name="Student_Agent",
            system_message="You are a student willing to learn.",
            llm_config=openai_gpt4o_mini_llm_config,
        )
        teacher_agent = ConversableAgent(
            name="Teacher_Agent",
            system_message="You are a math teacher.",
            llm_config=openai_gpt4o_mini_llm_config,
        )

        chat_result = student_agent.initiate_chat(
            teacher_agent,
            message=initial_message,
            summary_method="reflection_with_llm",
            max_turns=5,
        )

        return chat_result.summary  # type: ignore[no-any-return]

    initial_message = "What is triangle inequality?"

    name = "simple_learning"

    io = ConsoleUI()

    io.process_message(
        IOMessage.create(
            sender="user",
            recipient="workflow",
            type="system_message",
            message={
                "heading": "Workflow BEGIN",
                "body": f"Starting workflow with initial_message: {initial_message}",
            },
        )
    )

    result = wf.run(
        name=name,
        session_id="session_id",
        io=io.create_subconversation(),
        initial_message=initial_message,
    )

    io.process_message(
        IOMessage.create(
            sender="user",
            recipient="workflow",
            type="system_message",
            message={
                "heading": "Workflow END",
                "body": f"Ending workflow with result: {result}",
            },
        )
    )


@pytest.mark.openai
class TestAutoGenWorkflowsWithHumanInputAlways:
    @pytest.fixture
    def wf(self, openai_gpt4o_mini_llm_config: dict[str, Any]) -> AutoGenWorkflows:
        wf = AutoGenWorkflows()

        @wf.register(
            name="test_workflow",
            description="Test of user proxy with human input mode set to always",
        )
        def workflow(io: Chatable, initial_message: str, session_id: str) -> str:
            user_proxy = UserProxyAgent(
                name="User_Proxy",
                human_input_mode="ALWAYS",
            )
            assistant = ConversableAgent(
                name="Teacher_Agent",
                system_message="You are a math teacher.",
                llm_config=openai_gpt4o_mini_llm_config,
            )

            @user_proxy.register_for_execution()  # type: ignore[misc]
            @assistant.register_for_llm(description="Get weather information")  # type: ignore[misc]
            def get_weather_info(
                city: Annotated[
                    str, "city for which the weather information is requested"
                ],
            ) -> str:
                return "The weather in Zagreb right now is heavy rain."

            chat_result = user_proxy.initiate_chat(
                assistant,
                message=initial_message,
                summary_method="reflection_with_llm",
                max_turns=5,
            )

            return chat_result.summary  # type: ignore[no-any-return]

        return wf

    @pytest.mark.parametrize("response", ["", "Reject"])
    def test(
        self, wf: AutoGenWorkflows, response: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("builtins.input", InputMock([response] * 7))

        result = wf.run(
            name="test_workflow",
            session_id="session_id",
            io=ConsoleUI(),
            initial_message="What is the weather in Zagreb right now?",
        )

        assert result is not None
