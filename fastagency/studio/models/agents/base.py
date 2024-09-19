from typing import Annotated, Optional, Union
from uuid import UUID

from typing_extensions import TypeAlias

from fastagency.api.openapi import OpenAPI

from ..base import Field, Model
from ..registry import Registry
from ..toolboxes.toolbox import ToolboxRef

__all__ = ["AgentBaseModel"]

# Agents can work with any LLM, so we construct a union of all LLM references
llm_type_refs: TypeAlias = Union[  # type: ignore[valid-type]
    tuple(Registry.get_default().get_models_refs_by_type("llm"))
]


class AgentBaseModel(Model):
    llm: Annotated[
        llm_type_refs,
        Field(
            title="LLM",
            description="LLM used by the agent for producing responses",
            tooltip_message="Choose the LLM the agent will use to generate responses.",
        ),
    ]

    toolbox_1: Annotated[
        Optional[ToolboxRef],
        Field(
            title="Toolbox",
            description="Toolbox used by the agent for producing responses",
            tooltip_message="Choose the toolbox that the agent will use automatically when needed to solve user queries.",
        ),
    ] = None

    toolbox_2: Annotated[
        Optional[ToolboxRef],
        Field(
            title="Toolbox",
            description="Toolbox used by the agent for producing responses",
            tooltip_message="Choose the toolbox that the agent will use automatically when needed to solve user queries.",
        ),
    ] = None

    toolbox_3: Annotated[
        Optional[ToolboxRef],
        Field(
            title="Toolbox",
            description="Toolbox used by the agent for producing responses",
            tooltip_message="Choose the toolbox that the agent will use automatically when needed to solve user queries.",
        ),
    ] = None

    async def get_clients_from_toolboxes(self, user_id: UUID) -> list[OpenAPI]:
        clients: list[OpenAPI] = []
        for i in range(3):
            toolbox_property = getattr(self, f"toolbox_{i+1}")
            if toolbox_property is None:
                continue

            toolbox_model = await toolbox_property.get_data_model().from_db(
                toolbox_property.uuid
            )
            client = await toolbox_model.create_autogen(toolbox_property.uuid, user_id)
            clients.append(client)
        return clients
