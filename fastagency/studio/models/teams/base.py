import re
from typing import Annotated, Any, Literal, Union

from autogen.agentchat import ConversableAgent
from pydantic import Field
from typing_extensions import TypeAlias

from ..base import Model
from ..registry import Registry
from ..toolboxes.toolbox import OpenAPI

__all__ = ["TeamBaseModel", "agent_type_refs"]

# Agents can work with any LLM, so we construct a union of all LLM references
agent_type_refs: TypeAlias = Union[  # type: ignore[valid-type]
    tuple(Registry.get_default().get_models_refs_by_type("agent"))
]


class TeamBaseModel(Model):
    is_termination_msg_regex: Annotated[
        str,
        Field(
            description="Whether the message is a termination message or not. If it is a termination message, the chat will terminate."
        ),
    ] = "TERMINATE"

    human_input_mode: Annotated[
        Literal["ALWAYS", "TERMINATE", "NEVER"],
        Field(
            title="Human Input Mode",
            description="Mode for human input",
        ),
    ] = "ALWAYS"

    def is_termination_msg(self, msg: dict[str, Any]) -> bool:
        # print(f"is_termination_msg: {msg=}")
        return (
            "content" in msg
            and isinstance(msg["content"], str)
            and bool(re.findall(self.is_termination_msg_regex, msg["content"]))
        )


def register_toolbox_functions(
    agent: ConversableAgent,
    execution_agents: list[ConversableAgent],
    clients: list[OpenAPI],
) -> None:
    for client in clients:
        client.register_for_llm(agent)
        for execution_agent in execution_agents:
            client.register_for_execution(execution_agent)
