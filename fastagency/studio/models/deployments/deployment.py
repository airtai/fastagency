import re
from typing import Annotated, Any, Union
from uuid import UUID

from pydantic import field_validator
from typing_extensions import TypeAlias

from ..base import Field, Model
from ..registry import Registry
from ..secrets.fly_token import FlyToken
from ..secrets.github_token import GitHubToken

__all__ = ["Deployment"]

# Deployments can work with any Team, so we construct a union of all Team references
team_type_refs: TypeAlias = Union[  # type: ignore[valid-type]
    tuple(Registry.get_default().get_models_refs_by_type("team"))
]

# Deployments can work with any FlyIO Tokens, so we construct a union of all FlyIO Token references
FlyTokenRef: TypeAlias = FlyToken.get_reference_model()  # type: ignore[valid-type]

# Deployments can work with any GitHub Tokens, so we construct a union of all GitHub Token references
GitHubTokenRef: TypeAlias = GitHubToken.get_reference_model()  # type: ignore[valid-type]


@Registry.get_default().register("deployment")
class Deployment(Model):
    name: Annotated[
        str,
        Field(
            ...,
            description="The name of the SaaS application.",
            min_length=1,
            tooltip_message="The application name to be used in the deployed SaaS application.",
        ),
    ]

    repo_name: Annotated[
        str,
        Field(
            ...,
            description="The name of the GitHub repository.",
            min_length=1,
            immutable_after_creation=True,
            tooltip_message="The GitHub repository to be created. If the name contains spaces or special characters, GitHub will adjust it according to its naming rules. A random suffix will be added if the repository name already exists.",
        ),
    ]

    fly_app_name: Annotated[
        str,
        Field(
            ...,
            description="The name of the Fly.io application.",
            min_length=1,
            max_length=30,
            immutable_after_creation=True,
            tooltip_message="The Fly.io application. This will be used to create and deploy your React, Node.js, and PostgreSQL apps to Fly.io.",
        ),
    ]

    team: Annotated[
        team_type_refs,
        Field(
            title="Team Name",
            description="The team that is used in the deployment",
            tooltip_message="Choose the team to be used for deployment. User messages are sent to the Initial agent of the chosen team, and the agent's responses are sent back to the user. This field can be updated anytime to switch teams, with changes reflected in real-time in your deployments.",
        ),
    ]
    gh_token: Annotated[
        GitHubTokenRef,
        Field(
            title="GH Token",
            description="The GitHub token to use for creating a new repository",
            immutable_after_creation=True,
            tooltip_message="Choose the GitHub token used for authenticating and managing access to your GitHub account.",
        ),
    ]
    fly_token: Annotated[
        FlyTokenRef,
        Field(
            title="Fly Token",
            description="The Fly.io token to use for deploying the deployment",
            immutable_after_creation=True,
            tooltip_message="Choose the Fly.io token used for authenticating and managing access to your Fly.io account.",
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> Any:
        raise NotImplementedError

    @field_validator("fly_app_name")
    @classmethod
    def validate_fly_app_name(cls: type["Deployment"], value: Any) -> Any:
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9\- ]*$", value):
            raise ValueError(
                "Fly.io app name must contain only letters, numbers, spaces, dashes and should not start with a numeric literal. Example of a valid name: my-fly-app"
            )
        return value

    @field_validator("repo_name")
    @classmethod
    def validate_repo_name(cls: type["Deployment"], value: Any) -> Any:
        if not re.match(r"^[A-Za-z0-9._-]+$", value):
            raise ValueError(
                "The repository name can only contain ASCII letters, digits, and the characters ., -, and _. Example of a valid name: my-fa-repo"
            )
        return value
