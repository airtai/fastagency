import pytest

from fastagency.core.base import (
    FunctionCallExecutionContent,
    IOMessage,
    MultipleChoiceContent,
    SuggestedFunctionCallContent,
    TextInputContent,
    TextMessageContent,
)


class TestIOMessage:
    def test_init_without_params(self) -> None:
        msg = IOMessage()

        assert isinstance(msg, IOMessage)

        assert msg.sender is None
        assert msg.recepient is None
        assert msg.heading is None
        assert msg.type == "text_message"
        assert msg.content == TextMessageContent()

    def test_init_for_text_message(self) -> None:
        msg = IOMessage(
            sender="bot",
            recepient="user",
            heading="Greeting",
            type="text_message",
            content={"body": "Hello, world!"},
        )

        assert isinstance(msg, IOMessage)

        assert msg.sender == "bot"
        assert msg.recepient == "user"
        assert msg.heading == "Greeting"
        assert msg.type == "text_message"
        assert isinstance(msg.content, TextMessageContent)
        assert msg.content.body == "Hello, world!"

    def test_init_for_suggested_function_call(self) -> None:
        msg = IOMessage(
            sender="bot",
            recepient="user",
            heading="Greeting",
            type="suggested_function_call",
            content={
                "function_name": "greet",
                "arguments": {"name": "world", "time": "morning", "count": 1},
            },
        )

        assert isinstance(msg, IOMessage)

        assert msg.sender == "bot"
        assert msg.recepient == "user"
        assert msg.heading == "Greeting"
        assert msg.type == "suggested_function_call"
        assert isinstance(msg.content, SuggestedFunctionCallContent)
        assert msg.content.function_name == "greet"
        assert msg.content.arguments == {"name": "world", "time": "morning", "count": 1}

    def test_init_for_function_call_execution(self) -> None:
        msg = IOMessage(
            sender="bot",
            recepient="user",
            heading="Greeting",
            type="function_call_execution",
            content={
                "function_name": "greet",
                "retval": {"greeting": "Hello, world!"},
            },
        )

        assert isinstance(msg, IOMessage)

        assert msg.sender == "bot"
        assert msg.recepient == "user"
        assert msg.heading == "Greeting"
        assert msg.type == "function_call_execution"
        assert isinstance(msg.content, FunctionCallExecutionContent)
        assert msg.content.function_name == "greet"
        assert msg.content.retval == {"greeting": "Hello, world!"}

    def test_init_for_text_input(self) -> None:
        msg = IOMessage(
            sender="bot",
            recepient="user",
            heading="Greeting",
            type="text_input",
            content={"prompt": "What's your name?"},
        )

        assert isinstance(msg, IOMessage)

        assert msg.sender == "bot"
        assert msg.recepient == "user"
        assert msg.heading == "Greeting"
        assert msg.type == "text_input"
        assert isinstance(msg.content, TextInputContent)
        assert msg.content.prompt == "What's your name?"
        assert msg.content.suggestions == []
        assert msg.content.password is False

    def test_init_for_multiple_choice(self) -> None:
        msg = IOMessage(
            sender="bot",
            recepient="user",
            heading="Greeting",
            type="multiple_choice",
            content={
                "prompt": "What's your favorite color?",
                "choices": ["red", "green", "blue"],
                "default": "red",
                "single": True,
            },
        )

        assert isinstance(msg, IOMessage)

        assert msg.sender == "bot"
        assert msg.recepient == "user"
        assert msg.heading == "Greeting"
        assert msg.type == "multiple_choice"
        assert isinstance(msg.content, MultipleChoiceContent)
        assert msg.content.prompt == "What's your favorite color?"
        assert msg.content.choices == ["red", "green", "blue"]
        assert msg.content.default == "red"

    def test_init_for_invalid_type(self) -> None:
        with pytest.raises(KeyError) as exc_info:
            IOMessage(
                sender="bot",
                recepient="user",
                heading="Greeting",
                type="invalid_type",
            )

        assert str(exc_info.value) == "'invalid_type'"
