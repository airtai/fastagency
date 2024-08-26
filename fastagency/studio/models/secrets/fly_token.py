from typing import Annotated, Any
from uuid import UUID

from pydantic import Field

from ..base import Model
from ..registry import register

__all__ = ["FlyToken"]


@register("secret")
class FlyToken(Model):
    fly_token: Annotated[
        str,
        Field(
            title="Fly Token",
            description="The Fly.io token to use for deploying the deployment",
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model = await cls.from_db(model_id)

        return my_model.fly_token
