import asyncio
import re
from collections.abc import Iterable, Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Protocol,
    Union,
    runtime_checkable,
)

from autogen.agentchat import ConversableAgent
from autogen.events.base_event import get_event_classes

from ...base import (
    UI,
    WorkflowTypeVar,
    WorkflowsProtocol,
    check_register_decorator,
)
from ...logging import get_logger

if TYPE_CHECKING:
    from autogen.events.base_event import BaseEvent

    from fastagency.api.openapi import OpenAPI

__all__ = [
    "Workflow",
    "create_ag2_event",
]

# Populate ag2 event classes for each event type
EVENT_CLASSES = get_event_classes()

# Get the logger
logger = get_logger(__name__)

logger.info("Importing autogen.base.py")

_patterns = {
    "end_of_message": (
        "^\\n--------------------------------------------------------------------------------\\n$",
    ),
    "auto_reply": (
        "^\\x1b\\[31m\\n>>>>>>>> USING AUTO REPLY...\\x1b\\[0m\\n$",
        "^\\n>>>>>>>> USING AUTO REPLY...\\n$",
    ),
    "sender_recipient": (
        "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
        "^([a-zA-Z0-9_-]+) \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
    ),
    "suggested_function_call": (
        "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
        "^\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\n$",
    ),
    "stars": ("^\\x1b\\[32m(\\*{69}\\*+)\\x1b\\[0m\n$", "^(\\*{69}\\*+)\\n$"),
    "function_call_execution": (
        "^\\x1b\\[35m\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\x1b\\[0m\\n$",
        "^\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\n$",
    ),
    "response_from_calling_tool": (
        "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
        "^\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\n$",
    ),
    "no_human_input_received": (
        "^\\x1b\\[31m\\n>>>>>>>> NO HUMAN INPUT RECEIVED\\.\\x1b\\[0m$",
        "^\\n>>>>>>>> NO HUMAN INPUT RECEIVED\\.$",
    ),
    "user_interrupted": ("^USER INTERRUPTED\\n$",),
    "arguments": ("^Arguments: \\n(.*)\\n$",),
    "auto_reply_input": (
        "^Replying as ([a-zA-Z0-9_]+). Provide feedback to ([a-zA-Z0-9_]+). Press enter to skip and use auto-reply, or type 'exit' to end the conversation: $",
    ),
    "next_speaker": (
        "^Next speaker: [a-zA-Z0-9_]+$",
        "^\\u001b\\[32m\nNext speaker: [a-zA-Z0-9_]+\n\\u001b\\[0m$",
    ),
}


def _match(key: str, string: str, /) -> bool:
    return any(re.match(pattern, string) for pattern in _patterns[key])


def _findall(key: str, string: str, /) -> tuple[str, ...]:
    for pattern in _patterns[key]:
        if re.match(pattern, string):
            return re.findall(pattern, string)[0]  # type: ignore[no-any-return]
    return ()  # type: ignore[no-any-return]


def create_ag2_event(type: Optional[str] = None, **kwargs: Any) -> "BaseEvent":
    type = type or "text"
    if type not in EVENT_CLASSES:
        raise ValueError(f"Unknown event type: {type}")

    # Get the ag2 event class
    cls = EVENT_CLASSES[type]

    content = kwargs.pop("content", {})
    kwargs.update(content)

    return cls(**kwargs)


class Workflow(WorkflowsProtocol):
    def __init__(self) -> None:
        """Initialize the workflows."""
        self._workflows: dict[str, tuple[Callable[[UI, dict[str, Any]], str], str]] = {}

    def register(
        self, name: str, description: str, *, fail_on_redefintion: bool = False
    ) -> Callable[[WorkflowTypeVar], WorkflowTypeVar]:
        def decorator(func: WorkflowTypeVar) -> WorkflowTypeVar:
            check_register_decorator(func)
            if name in self._workflows:
                if fail_on_redefintion:
                    raise ValueError(f"A workflow with name '{name}' already exists.")
                else:
                    logger.warning(f"Overwriting workflow with name '{name}'")

            self._workflows[name] = func, description
            return func

        return decorator

    def run(
        self,
        name: str,
        ui: UI,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        workflow, _ = self._workflows[name]

        # todo: inject user_id into call (and other stuff)
        try:
            ui.workflow_started(
                sender="Workflow",
                recipient="User",
                name=name,
                description=self.get_description(name),
                params=kwargs,
            )
            retval = (
                asyncio.run(workflow(ui, kwargs))
                if asyncio.iscoroutinefunction(workflow)
                else workflow(ui, kwargs)
            )

        except Exception as e:
            logger.error(
                f"Unhandled exception occurred when executing the workflow: {e}",
                exc_info=True,
            )
            ui.error(
                sender="Workflow",
                recipient="User",
                short="Unhandled exception occurred when executing the workflow.",
                long=str(e),
            )
            retval = f"Unhandled exception occurred when executing the workflow: {e}"

        ui.workflow_completed(
            sender="Workflow",
            recipient="User",
            result=retval,
        )
        logger.info(f"Workflow '{name}' completed with result: {retval}")

        return retval

    @property
    def names(self) -> list[str]:
        return list(self._workflows.keys())

    def get_description(self, name: str) -> str:
        _, description = self._workflows.get(name, (None, "Description not available!"))
        return description

    def register_api(
        self,
        api: "OpenAPI",
        callers: Union[ConversableAgent, Iterable[ConversableAgent]],
        executors: Union[ConversableAgent, Iterable[ConversableAgent]],
        functions: Optional[
            Union[str, Iterable[Union[str, Mapping[str, Mapping[str, str]]]]]
        ] = None,
    ) -> None:
        if not isinstance(callers, Iterable):
            callers = [callers]
        if not isinstance(executors, Iterable):
            executors = [executors]
        if isinstance(functions, str):
            functions = [functions]

        for caller in callers:
            api._register_for_llm(caller, functions=functions)

        for executor in executors:
            api._register_for_execution(executor, functions=functions)


@runtime_checkable
class Toolable(Protocol):
    def register(
        self,
        *,
        caller: ConversableAgent,
        executor: Union[ConversableAgent, list[ConversableAgent]],
    ) -> None: ...
