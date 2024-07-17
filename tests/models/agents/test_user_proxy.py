import uuid

import autogen
import pytest
from fastapi import BackgroundTasks

from fastagency.app import add_model
from fastagency.models.agents.user_proxy import UserProxyAgent


class TestUserProxyAgent:
    @pytest.mark.asyncio()
    @pytest.mark.db()
    async def test_user_proxy_model_create_autogen(
        self,
        user_uuid: str,
    ) -> None:
        user_proxy_model = UserProxyAgent(
            name="User proxy",
            system_message="test system message",
        )
        user_proxy_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="agent",
            model_name=UserProxyAgent.__name__,
            model_uuid=user_proxy_model_uuid,
            model=user_proxy_model.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        agent, functions = await UserProxyAgent.create_autogen(
            model_id=uuid.UUID(user_proxy_model_uuid),
            user_id=uuid.UUID(user_uuid),
        )
        assert isinstance(agent, autogen.agentchat.UserProxyAgent)
        assert functions == []
