from typing import Annotated, Any
from uuid import UUID

from autogen import ConversableAgent
from pydantic import Field

from ..registry import Registry
from ..toolboxes.toolbox import OpenAPI
from .base import TeamBaseModel, agent_type_refs, register_toolbox_functions

__all__ = ["TwoAgentTeam"]


class AutogenTwoAgentTeam:
    def __init__(
        self,
        *,
        initial_agent: ConversableAgent,
        initial_agent_clients: list[OpenAPI],
        secondary_agent: ConversableAgent,
        secondary_agent_clients: list[OpenAPI],
    ) -> None:
        self.initial_agent = initial_agent
        self.secondary_agent = secondary_agent

        register_toolbox_functions(
            initial_agent, [secondary_agent], initial_agent_clients
        )
        register_toolbox_functions(
            secondary_agent, [initial_agent], secondary_agent_clients
        )

    def initiate_chat(self, message: str) -> list[dict[str, Any]]:
        return self.initial_agent.initiate_chat(  # type: ignore[no-any-return]
            recipient=self.secondary_agent, message=message
        )


@Registry.get_default().register("team")
class TwoAgentTeam(TeamBaseModel):
    initial_agent: Annotated[
        agent_type_refs,
        Field(
            title="Initial Agent",
            description="Agent that starts the conversation",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Select the Initial Agent, the agent responsible for task orchestration. It interacts with users and assigns tasks to Secondary Agent, enhancing the efficiency of complex operations."
                }
            },
        ),
    ]
    secondary_agent: Annotated[
        agent_type_refs,
        Field(
            title="Secondary Agent",
            description="Agent that continues the conversation",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Select the Secondary Agent, the agent responsible for collaborating with the Initial Agent in performing specialized tasks. Secondary Agents enhance efficiency by focusing on specific roles, such as data analysis or code execution."
                }
            },
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> Any:
        my_model = await cls.from_db(model_id)

        is_termination_msg = my_model.is_termination_msg
        human_input_mode = my_model.human_input_mode

        initial_agent_model = await my_model.initial_agent.get_data_model().from_db(
            my_model.initial_agent.uuid
        )
        (
            initial_agent,
            initial_agent_clients,
        ) = await initial_agent_model.create_autogen(
            my_model.initial_agent.uuid,
            user_id,
            is_termination_msg=is_termination_msg,
            human_input_mode=human_input_mode,
        )

        secondary_agent_model = await my_model.secondary_agent.get_data_model().from_db(
            my_model.secondary_agent.uuid
        )
        (
            secondary_agent,
            secondary_agent_clients,
        ) = await secondary_agent_model.create_autogen(
            my_model.secondary_agent.uuid,
            user_id,
            is_termination_msg=is_termination_msg,
            human_input_mode=human_input_mode,
        )

        return AutogenTwoAgentTeam(
            initial_agent=initial_agent,
            initial_agent_clients=initial_agent_clients,
            secondary_agent=secondary_agent,
            secondary_agent_clients=secondary_agent_clients,
        )
