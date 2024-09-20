import pytest

from fastagency.runtime.autogen.agents.web_surfer import (
    WebSurferChat,
)
from tests.helpers import get_by_tag, parametrize_fixtures


class TestWebSurferChat:
    @parametrize_fixtures("websurfer_chat", get_by_tag("websurfer-chat"))
    def test_web_surfer_chat_constructor(
        self,
        websurfer_chat: WebSurferChat,
    ) -> None:
        assert isinstance(websurfer_chat, WebSurferChat)

    @parametrize_fixtures("websurfer_chat", get_by_tag("websurfer-chat"))
    @pytest.mark.parametrize(
        "task",
        [
            "Visit https://en.wikipedia.org/wiki/Zagreb and tell me when Zagreb became a free royal city.",
            # "What is the most expensive NVIDIA GPU on https://www.alternate.de/ and how much it costs?",
            # "Compile a list of news headlines under section 'Politika i kriminal' on telegram.hr.",
            # "What is the single the most newsworthy story today?",
            # "Given that weather forecast today is warm and sunny, what would be the best way to spend an evening in Zagreb according to the weather forecast?",
        ],
    )
    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_web_surfer_chat_simple_task(
        self, websurfer_chat: WebSurferChat, task: str
    ) -> None:
        result: str = await websurfer_chat.create_new_task(task=task)
        print(result)  # noqa: T201
        assert isinstance(result, str)
        assert "We have successfully completed the task" in result

    @parametrize_fixtures("websurfer_chat", get_by_tag("websurfer-chat"))
    @pytest.mark.parametrize(
        ("task", "follow_up"),
        [
            (
                "What is the most expensive NVIDIA GPU on https://www.alternate.de/ and how much it costs?",
                "What is the second most expensive one and what's the price?",
            ),
        ],
    )
    @pytest.mark.llm
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="This test is not working properly in CI")
    async def test_web_surfer_chat_complex_task(
        self, websurfer_chat: WebSurferChat, task: str, follow_up: str
    ) -> None:
        result: str = await websurfer_chat.create_new_task(task=task)
        print(result)  # noqa: T201
        assert isinstance(result, str)
        assert "We have successfully completed the task" in result
        assert "NVIDIA" in result

        result = await websurfer_chat.continue_task_with_additional_instructions(
            message=follow_up
        )
        print(result)  # noqa: T201
        assert isinstance(result, str)
        assert "We have successfully completed the task" in result
        assert "NVIDIA" in result
