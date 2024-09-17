from typing import Annotated, Any
from uuid import UUID

from ..base import Field, Model
from ..registry import register

__all__ = ["FlyToken"]


@register("secret")
class FlyToken(Model):
    fly_token: Annotated[
        str,
        Field(
            title="Fly Token",
            description="The Fly.io token to use for deploying the deployment",
            tooltip_message="The token specified here will be used to authenticate your access to Fly.io services.",
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model = await cls.from_db(model_id)

        return my_model.fly_token
