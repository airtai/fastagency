from typing import Annotated, Any, Optional
from uuid import UUID

import autogen
from pydantic import Field

from ....api.openapi import OpenAPI
from ..base import Model
from ..registry import register


@register("agent")
class UserProxyAgent(Model):
    max_consecutive_auto_reply: Annotated[
        Optional[int],
        Field(
            description="The maximum number of consecutive auto-replies the agent can make",
            json_schema_extra={
                "metadata": {
                    "tooltip_message": "Set the maximum number of consecutive auto replies the agent can make before requiring human approval. A higher value gives the agent more autonomy, while leaving it blank prompts permission for each reply. For example, if you set this to 2, the agent will reply twice and then require human approval before replying again."
                }
            },
        ),
    ] = None

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> tuple[autogen.agentchat.AssistantAgent, list[OpenAPI]]:
        my_model = await cls.from_db(model_id)

        agent_name = my_model.name

        agent = autogen.agentchat.UserProxyAgent(
            name=agent_name,
            max_consecutive_auto_reply=my_model.max_consecutive_auto_reply,
            code_execution_config=False,
            **kwargs,
        )
        return agent, []
