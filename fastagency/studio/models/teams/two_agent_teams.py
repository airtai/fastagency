from typing import Annotated, Any, Dict, List
from uuid import UUID

from autogen import ConversableAgent
from pydantic import Field

from ..registry import Registry
from ..toolboxes.toolbox import Client
from .base import TeamBaseModel, agent_type_refs, register_toolbox_functions

__all__ = ["TwoAgentTeam"]


class AutogenTwoAgentTeam:
    def __init__(
        self,
        *,
        initial_agent: ConversableAgent,
        initial_agent_clients: List[Client],
        secondary_agent: ConversableAgent,
        secondary_agent_clients: List[Client],
    ) -> None:
        self.initial_agent = initial_agent
        self.secondary_agent = secondary_agent

        register_toolbox_functions(
            initial_agent, [secondary_agent], initial_agent_clients
        )
        register_toolbox_functions(
            secondary_agent, [initial_agent], secondary_agent_clients
        )

    def initiate_chat(self, message: str) -> List[Dict[str, Any]]:
        return self.initial_agent.initiate_chat(  # type: ignore[no-any-return]
            recipient=self.secondary_agent, message=message
        )


@Registry.get_default().register("team")
class TwoAgentTeam(TeamBaseModel):
    initial_agent: Annotated[
        agent_type_refs,
        Field(
            title="Initial agent",
            description="Agent that starts the conversation",
        ),
    ]
    secondary_agent: Annotated[
        agent_type_refs,
        Field(
            title="Secondary agent",
            description="Agent that continues the conversation",
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
