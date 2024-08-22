import uuid
from typing import Any, Dict

import pytest
from fastapi import BackgroundTasks

from fastagency.app import add_model
from fastagency.models.base import Model
from fastagency.models.secrets.fly_token import FlyToken


class TestFlyToken:
    def test_constructor_success(self) -> None:
        fly_token = FlyToken(
            fly_token="*" * 64,  # pragma: allowlist secret
            name="Hello World!",
        )  # pragma: allowlist secret
        assert (
            fly_token.fly_token == "*" * 64  # pragma: allowlist secret
        )  # pragma: allowlist secret

    @pytest.mark.asyncio
    @pytest.mark.db
    @pytest.mark.parametrize("fly_token_model", [(FlyToken)])
    async def test_github_token_model_create_autogen(
        self,
        fly_token_model: Model,
        azure_gpt35_turbo_16k_llm_config: Dict[str, Any],
        user_uuid: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        dummy_github_token = "*" * 64  # pragma: allowlist secret

        # Add secret to database
        fly_token = fly_token_model(  # type: ignore [operator]
            fly_token=dummy_github_token,
            name="fly_token_model_name",
        )
        fly_token_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="secret",
            model_name=fly_token_model.__name__,  # type: ignore [attr-defined]
            model_uuid=fly_token_model_uuid,
            model=fly_token.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        # Call create_autogen
        actual_fly_token = await FlyToken.create_autogen(
            model_id=uuid.UUID(fly_token_model_uuid),
            user_id=uuid.UUID(user_uuid),
        )
        assert isinstance(actual_fly_token, str)
        assert actual_fly_token == fly_token.fly_token
