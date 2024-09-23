from typing import Annotated, Any
from uuid import UUID

from ..base import Field, Model
from ..registry import register

__all__ = ["GitHubToken"]


@register("secret")
class GitHubToken(Model):
    gh_token: Annotated[
        str,
        Field(
            title="GH Token",
            description="The GitHub token to use for creating a new repository",
            tooltip_message="The token specified here will be used to authenticate your access to GitHub services.",
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model = await cls.from_db(model_id)

        return my_model.gh_token
