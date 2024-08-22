import uuid
from typing import Any, Dict

import pytest
from fastapi import BackgroundTasks

from fastagency.studio.app import add_model
from fastagency.studio.models.base import Model
from fastagency.studio.models.secrets.github_token import GitHubToken


class TestGitHubToken:
    def test_constructor_success(self) -> None:
        gh_token = GitHubToken(
            gh_token="*" * 64,  # pragma: allowlist secret
            name="Hello World!",
        )  # pragma: allowlist secret
        assert (
            gh_token.gh_token == "*" * 64  # pragma: allowlist secret
        )  # pragma: allowlist secret

    @pytest.mark.asyncio
    @pytest.mark.db
    @pytest.mark.parametrize("gh_token_model", [(GitHubToken)])
    async def test_github_token_model_create_autogen(
        self,
        gh_token_model: Model,
        azure_gpt35_turbo_16k_llm_config: Dict[str, Any],
        user_uuid: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        dummy_github_token = "*" * 64  # pragma: allowlist secret

        # Add secret to database
        gh_token = gh_token_model(  # type: ignore [operator]
            gh_token=dummy_github_token,
            name="gh_token_model_name",
        )
        gh_token_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="secret",
            model_name=gh_token_model.__name__,  # type: ignore [attr-defined]
            model_uuid=gh_token_model_uuid,
            model=gh_token.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        # Call create_autogen
        actual_gh_token = await GitHubToken.create_autogen(
            model_id=uuid.UUID(gh_token_model_uuid),
            user_id=uuid.UUID(user_uuid),
        )
        assert isinstance(actual_gh_token, str)
        assert actual_gh_token == gh_token.gh_token
