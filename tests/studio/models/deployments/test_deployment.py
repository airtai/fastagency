import json
import uuid

import jsondiff
import pytest
from pydantic import ValidationError

from fastagency.studio.models.base import Model
from fastagency.studio.models.deployments.deployment import Deployment
from fastagency.studio.models.secrets.fly_token import FlyToken
from fastagency.studio.models.secrets.github_token import GitHubToken
from fastagency.studio.models.teams.multi_agent_team import MultiAgentTeam
from fastagency.studio.models.teams.two_agent_teams import TwoAgentTeam


class TestDeployment:
    @pytest.mark.parametrize(
        "team_model",
        [TwoAgentTeam, pytest.param(MultiAgentTeam, marks=pytest.mark.skip)],
    )
    @pytest.mark.parametrize("gh_token_model", [(GitHubToken)])
    @pytest.mark.parametrize("fly_token_model", [(FlyToken)])
    def test_deployment_constructor(
        self, team_model: Model, gh_token_model: Model, fly_token_model: Model
    ) -> None:
        team_uuid = uuid.uuid4()
        team = team_model.get_reference_model()(uuid=team_uuid)

        gh_token_uuid = uuid.uuid4()
        gh_token = gh_token_model.get_reference_model()(uuid=gh_token_uuid)

        fly_token_uuid = uuid.uuid4()
        fly_token = fly_token_model.get_reference_model()(uuid=fly_token_uuid)

        try:
            deployment = Deployment(
                team=team,
                name="Test Deployment",
                repo_name="test-deployment",
                fly_app_name="test-deployment",
                gh_token=gh_token,
                fly_token=fly_token,
            )
        except ValidationError:
            # print(f"{e.errors()=}")
            raise

        assert deployment.team == team

    def test_deployment_model_schema(self, pydantic_version: float) -> None:
        schema = Deployment.model_json_schema()
        expected = {
            "$defs": {
                "FlyTokenRef": {
                    "properties": {
                        "type": {
                            "const": "secret",
                            "default": "secret",
                            "description": "The name of the type of the data",
                            "enum": ["secret"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "FlyToken",
                            "default": "FlyToken",
                            "description": "The name of the data",
                            "enum": ["FlyToken"],
                            "title": "Name",
                            "type": "string",
                        },
                        "uuid": {
                            "description": "The unique identifier",
                            "format": "uuid",
                            "title": "UUID",
                            "type": "string",
                        },
                    },
                    "required": ["uuid"],
                    "title": "FlyTokenRef",
                    "type": "object",
                },
                "GitHubTokenRef": {
                    "properties": {
                        "type": {
                            "const": "secret",
                            "default": "secret",
                            "description": "The name of the type of the data",
                            "enum": ["secret"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "GitHubToken",
                            "default": "GitHubToken",
                            "description": "The name of the data",
                            "enum": ["GitHubToken"],
                            "title": "Name",
                            "type": "string",
                        },
                        "uuid": {
                            "description": "The unique identifier",
                            "format": "uuid",
                            "title": "UUID",
                            "type": "string",
                        },
                    },
                    "required": ["uuid"],
                    "title": "GitHubTokenRef",
                    "type": "object",
                },
                "TwoAgentTeamRef": {
                    "properties": {
                        "type": {
                            "const": "team",
                            "default": "team",
                            "description": "The name of the type of the data",
                            "enum": ["team"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "TwoAgentTeam",
                            "default": "TwoAgentTeam",
                            "description": "The name of the data",
                            "enum": ["TwoAgentTeam"],
                            "title": "Name",
                            "type": "string",
                        },
                        "uuid": {
                            "description": "The unique identifier",
                            "format": "uuid",
                            "title": "UUID",
                            "type": "string",
                        },
                    },
                    "required": ["uuid"],
                    "title": "TwoAgentTeamRef",
                    "type": "object",
                },
            },
            "properties": {
                "name": {
                    "description": "The application name to use on the website.",
                    "minLength": 1,
                    "title": "Name",
                    "type": "string",
                },
                "repo_name": {
                    "description": "The name of the GitHub repository.",
                    "metadata": {"immutable_after_creation": True},
                    "minLength": 1,
                    "title": "Repo Name",
                    "type": "string",
                },
                "fly_app_name": {
                    "description": "The name of the Fly.io application.",
                    "maxLength": 30,
                    "metadata": {"immutable_after_creation": True},
                    "minLength": 1,
                    "title": "Fly App Name",
                    "type": "string",
                },
                "team": {
                    "$ref": "#/$defs/TwoAgentTeamRef",
                    "description": "The team that is used in the deployment",
                    "title": "Team Name",
                },
                "gh_token": {
                    "$ref": "#/$defs/GitHubTokenRef",
                    "description": "The GitHub token to use for creating a new repository",
                    "metadata": {"immutable_after_creation": True},
                    "title": "GH Token",
                },
                "fly_token": {
                    "$ref": "#/$defs/FlyTokenRef",
                    "description": "The Fly.io token to use for deploying the deployment",
                    "metadata": {"immutable_after_creation": True},
                    "title": "Fly Token",
                },
            },
            "required": [
                "name",
                "repo_name",
                "fly_app_name",
                "team",
                "gh_token",
                "fly_token",
            ],
            "title": "Deployment",
            "type": "object",
        }
        # print(schema)
        pydantic28_delta = '{"properties": {"team": {"allOf": [{"$$ref": "#/$defs/TwoAgentTeamRef"}], "$delete": ["$$ref"]}, "gh_token": {"allOf": [{"$$ref": "#/$defs/GitHubTokenRef"}], "$delete": ["$$ref"]}, "fly_token": {"allOf": [{"$$ref": "#/$defs/FlyTokenRef"}], "$delete": ["$$ref"]}}}'
        if pydantic_version < 2.9:
            # print(f"pydantic28_delta = '{jsondiff.diff(expected, schema, dump=True)}'")
            expected = jsondiff.patch(json.dumps(expected), pydantic28_delta, load=True)
        assert schema == expected

    @pytest.mark.parametrize(
        "team_model",
        [TwoAgentTeam, pytest.param(MultiAgentTeam, marks=pytest.mark.skip)],
    )
    @pytest.mark.parametrize("gh_token_model", [(GitHubToken)])
    @pytest.mark.parametrize("fly_token_model", [(FlyToken)])
    def test_assistant_model_validation(
        self, team_model: Model, gh_token_model: Model, fly_token_model: Model
    ) -> None:
        team_uuid = uuid.uuid4()
        team = team_model.get_reference_model()(uuid=team_uuid)

        gh_token_uuid = uuid.uuid4()
        gh_token = gh_token_model.get_reference_model()(uuid=gh_token_uuid)

        fly_token_uuid = uuid.uuid4()
        fly_token = fly_token_model.get_reference_model()(uuid=fly_token_uuid)

        deployment = Deployment(
            team=team,
            name="Test Deployment",
            repo_name="test-deployment",
            fly_app_name="test-deployment",
            gh_token=gh_token,
            fly_token=fly_token,
        )

        deployment_json = deployment.model_dump_json()
        # print(f"{deployment_json=}")
        assert deployment_json is not None

        validated_deployment = Deployment.model_validate_json(deployment_json)
        # print(f"{validated_agent=}")
        assert validated_deployment is not None
        assert validated_deployment == deployment

    @pytest.mark.parametrize(
        "fly_app_name", ["", "app_name", "123-app-name", "2024-06-29"]
    )
    def test_invalid_fly_io_app_name(self, fly_app_name: str) -> None:
        with pytest.raises(ValidationError):
            Deployment(
                team=TwoAgentTeam.get_reference_model()(uuid=uuid.uuid4()),
                name="Test Deployment",
                repo_name="test-deployment",
                fly_app_name=fly_app_name,
                gh_token=GitHubToken.get_reference_model()(uuid=uuid.uuid4()),
                fly_token=FlyToken.get_reference_model()(uuid=uuid.uuid4()),
            )

    @pytest.mark.parametrize("repo_name", ["repo name", "repo@name", "repo/name"])
    def test_invalid_repo_name(self, repo_name: str) -> None:
        with pytest.raises(
            ValueError, match="The repository name can only contain ASCII letters"
        ):
            Deployment(
                team=TwoAgentTeam.get_reference_model()(uuid=uuid.uuid4()),
                name="Test Deployment",
                repo_name=repo_name,
                fly_app_name="fly-app-name",
                gh_token=GitHubToken.get_reference_model()(uuid=uuid.uuid4()),
                fly_token=FlyToken.get_reference_model()(uuid=uuid.uuid4()),
            )

    @pytest.mark.parametrize("fly_app_name", ["app-name", "fa-123-app-name"])
    def test_valid_fly_io_app_name(self, fly_app_name: str) -> None:
        Deployment(
            team=TwoAgentTeam.get_reference_model()(uuid=uuid.uuid4()),
            name="Test Deployment",
            repo_name="test-deployment",
            fly_app_name=fly_app_name,
            gh_token=GitHubToken.get_reference_model()(uuid=uuid.uuid4()),
            fly_token=FlyToken.get_reference_model()(uuid=uuid.uuid4()),
        )
