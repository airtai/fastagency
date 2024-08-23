import uuid
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from fastagency.studio.models.agents.assistant import AssistantAgent
from fastagency.studio.models.agents.web_surfer import WebSurferAgent
from fastagency.studio.models.base import Model
from fastagency.studio.models.llms.azure import AzureOAI, AzureOAIAPIKey
from fastagency.studio.models.llms.openai import OpenAI
from fastagency.studio.models.teams.multi_agent_team import MultiAgentTeam


@pytest.mark.skip(reason="Temporarily disabling multi agent team")
class TestMultiAgentTeam:
    @pytest.mark.parametrize("llm_model", [OpenAI, AzureOAI])
    def test_multi_agent_constructor(self, llm_model: Model) -> None:
        llm_uuid = uuid.uuid4()
        llm = llm_model.get_reference_model()(uuid=llm_uuid)

        summarizer_llm_uuid = uuid.uuid4()
        summarizer_llm = llm_model.get_reference_model()(uuid=summarizer_llm_uuid)

        assistant_1 = AssistantAgent(
            llm=llm, name="Assistant", system_message="test system message"
        )
        assistant_2 = AssistantAgent(
            llm=llm, name="Assistant", system_message="test system message"
        )
        web_surfer = WebSurferAgent(
            name="WebSurfer", llm=llm, summarizer_llm=summarizer_llm
        )

        assistant_1_uuid = uuid.uuid4()
        assistant_1_ref = assistant_1.get_reference_model()(uuid=assistant_1_uuid)
        assistant_2_uuid = uuid.uuid4()
        assistant_2_ref = assistant_2.get_reference_model()(uuid=assistant_2_uuid)
        web_surfer_uuid = uuid.uuid4()
        web_surfer_ref = web_surfer.get_reference_model()(uuid=web_surfer_uuid)

        try:
            team = MultiAgentTeam(
                name="MultiAgentTeam",
                agent_1=assistant_1_ref,
                agent_2=assistant_2_ref,
                web_surfer_ref=web_surfer_ref,
            )
        except ValidationError:
            # print(f"{e.errors()=}")
            raise

        assert team

    def test_multi_agent_model_schema(self) -> None:
        schema = MultiAgentTeam.model_json_schema()
        expected = {
            "$defs": {
                "AssistantAgentRef": {
                    "properties": {
                        "type": {
                            "const": "agent",
                            "default": "agent",
                            "description": "The name of the type of the data",
                            "enum": ["agent"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "AssistantAgent",
                            "default": "AssistantAgent",
                            "description": "The name of the data",
                            "enum": ["AssistantAgent"],
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
                    "title": "AssistantAgentRef",
                    "type": "object",
                },
                "UserProxyAgentRef": {
                    "properties": {
                        "type": {
                            "const": "agent",
                            "default": "agent",
                            "description": "The name of the type of the data",
                            "enum": ["agent"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "UserProxyAgent",
                            "default": "UserProxyAgent",
                            "description": "The name of the data",
                            "enum": ["UserProxyAgent"],
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
                    "title": "UserProxyAgentRef",
                    "type": "object",
                },
                "WebSurferAgentRef": {
                    "properties": {
                        "type": {
                            "const": "agent",
                            "default": "agent",
                            "description": "The name of the type of the data",
                            "enum": ["agent"],
                            "title": "Type",
                            "type": "string",
                        },
                        "name": {
                            "const": "WebSurferAgent",
                            "default": "WebSurferAgent",
                            "description": "The name of the data",
                            "enum": ["WebSurferAgent"],
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
                    "title": "WebSurferAgentRef",
                    "type": "object",
                },
            },
            "properties": {
                "name": {
                    "description": "The name of the item",
                    "minLength": 1,
                    "title": "Name",
                    "type": "string",
                },
                "termination_message_regex": {
                    "default": "^TERMINATE$",
                    "description": "Whether the message is a termination message or not. If it is a termination message, the agent will not respond to it.",
                    "title": "Termination Message Regex",
                    "type": "string",
                },
                "human_input_mode": {
                    "default": "ALWAYS",
                    "description": "Mode for human input",
                    "enum": ["ALWAYS", "TERMINATE", "NEVER"],
                    "title": "Human input mode",
                    "type": "string",
                },
                "agent_1": {
                    "anyOf": [
                        {"$ref": "#/$defs/AssistantAgentRef"},
                        {"$ref": "#/$defs/UserProxyAgentRef"},
                        {"$ref": "#/$defs/WebSurferAgentRef"},
                    ],
                    "description": "An agent in the team",
                    "title": "Agents",
                },
                "agent_2": {
                    "anyOf": [
                        {"$ref": "#/$defs/AssistantAgentRef"},
                        {"$ref": "#/$defs/UserProxyAgentRef"},
                        {"$ref": "#/$defs/WebSurferAgentRef"},
                    ],
                    "description": "An agent in the team",
                    "title": "Agents",
                },
                "agent_3": {
                    "anyOf": [
                        {"$ref": "#/$defs/AssistantAgentRef"},
                        {"$ref": "#/$defs/UserProxyAgentRef"},
                        {"$ref": "#/$defs/WebSurferAgentRef"},
                        {"type": "null"},
                    ],
                    "default": None,
                    "description": "An agent in the team",
                    "title": "Agents",
                },
                "agent_4": {
                    "anyOf": [
                        {"$ref": "#/$defs/AssistantAgentRef"},
                        {"$ref": "#/$defs/UserProxyAgentRef"},
                        {"$ref": "#/$defs/WebSurferAgentRef"},
                        {"type": "null"},
                    ],
                    "default": None,
                    "description": "An agent in the team",
                    "title": "Agents",
                },
                "agent_5": {
                    "anyOf": [
                        {"$ref": "#/$defs/AssistantAgentRef"},
                        {"$ref": "#/$defs/UserProxyAgentRef"},
                        {"$ref": "#/$defs/WebSurferAgentRef"},
                        {"type": "null"},
                    ],
                    "default": None,
                    "description": "An agent in the team",
                    "title": "Agents",
                },
            },
            "required": ["name", "agent_1", "agent_2"],
            "title": "MultiAgentTeam",
            "type": "object",
        }
        # print(f"{schema=}")
        assert schema == expected

    @pytest.mark.parametrize("llm_model", [OpenAI, AzureOAI])
    def test_multi_agent_model_validation(self, llm_model: Model) -> None:
        llm_uuid = uuid.uuid4()
        llm = llm_model.get_reference_model()(uuid=llm_uuid)

        summarizer_llm_uuid = uuid.uuid4()
        summarizer_llm = llm_model.get_reference_model()(uuid=summarizer_llm_uuid)

        assistant_1 = AssistantAgent(
            llm=llm, name="Assistant", system_message="test system message"
        )
        assistant_2 = AssistantAgent(
            llm=llm, name="Assistant", system_message="test system message"
        )
        web_surfer = WebSurferAgent(
            name="WebSurfer", llm=llm, summarizer_llm=summarizer_llm
        )

        assistant_1_uuid = uuid.uuid4()
        assistant_1_ref = assistant_1.get_reference_model()(uuid=assistant_1_uuid)
        assistant_2_uuid = uuid.uuid4()
        assistant_2_ref = assistant_2.get_reference_model()(uuid=assistant_2_uuid)
        web_surfer_uuid = uuid.uuid4()
        web_surfer_ref = web_surfer.get_reference_model()(uuid=web_surfer_uuid)

        team = MultiAgentTeam(
            name="MultiAgentTeam",
            agent_1=assistant_1_ref,
            agent_2=assistant_2_ref,
            web_surfer_ref=web_surfer_ref,
        )

        team_json = team.model_dump_json()
        assert team_json is not None

        validated_team = MultiAgentTeam.model_validate_json(team_json)
        assert validated_team is not None
        assert validated_team == team

    @pytest.mark.skip(reason="Temporarily disabling multi agent team")
    @pytest.mark.asyncio
    @pytest.mark.db
    @pytest.mark.parametrize("enable_monkeypatch", [True, False])
    @pytest.mark.parametrize(
        "llm_model,api_key_model",  # noqa: PT006
        [
            (AzureOAI, AzureOAIAPIKey),
        ],
    )
    async def test_multi_agent_team_autogen(
        self,
        enable_monkeypatch: bool,
        llm_model: Model,
        api_key_model: Model,
        azure_gpt35_turbo_16k_llm_config: Dict[str, Any],
        user_uuid: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        pass
        # Add secret, llm, agent, team to database
        # api_key = api_key_model(  # type: ignore [operator]
        #     api_key = os.getenv("AZURE_OPENAI_API_KEY", default="*" * 64),
        #     name="api_key_model_name",
        # )
        # api_key_model_uuid = str(uuid.uuid4())
        # await add_model(
        #     user_uuid=user_uuid,
        #     type_name="secret",
        #     model_name=api_key_model.__name__,  # type: ignore [attr-defined]
        #     model_uuid=api_key_model_uuid,
        #     model=api_key.model_dump(),
        # )

        # llm = llm_model(  # type: ignore [operator]
        #     name="llm_model_name",
        #     model=os.getenv(AZURE_GPT35_MODEL, default="gpt-35-turbo-16k"),
        #     api_key=api_key.get_reference_model()(uuid=api_key_model_uuid),
        #     base_url=os.getenv(
        # "AZURE_API_ENDPOINT", default="https://my-deployment.openai.azure.com"

    # ),
    #     api_version=os.getenv("AZURE_API_VERSION", default="2024-02-01"),
    # )
    # llm_model_uuid = str(uuid.uuid4())
    # await add_model(
    #     user_uuid=user_uuid,
    #     type_name="llm",
    #     model_name=llm_model.__name__,  # type: ignore [attr-defined]
    #     model_uuid=llm_model_uuid,
    #     model=llm.model_dump(),
    # )

    # user_proxy_model = UserProxyAgent(
    #     name="UserProxyAgent",
    #     llm=llm.get_reference_model()(uuid=llm_model_uuid),
    # )
    # user_proxy_model_uuid = str(uuid.uuid4())
    # await add_model(
    #     user_uuid=user_uuid,
    #     type_name="agent",
    #     model_name=UserProxyAgent.__name__,
    #     model_uuid=user_proxy_model_uuid,
    #     model=user_proxy_model.model_dump(),
    # )

    # weatherman_assistant_model_1 = AssistantAgent(
    #     llm=llm.get_reference_model()(uuid=llm_model_uuid),
    #     name="Assistant",
    #     system_message="test system message",
    # )
    # weatherman_assistant_model_1_uuid = str(uuid.uuid4())
    # await add_model(
    #     user_uuid=user_uuid,
    #     type_name="agent",
    #     model_name=AssistantAgent.__name__,
    #     model_uuid=weatherman_assistant_model_1_uuid,
    #     model=weatherman_assistant_model_1.model_dump(),
    # )

    # team_model_uuid = str(uuid.uuid4())
    # agent_1 = user_proxy_model.get_reference_model()(uuid=user_proxy_model_uuid)
    # agent_2 = weatherman_assistant_model_1.get_reference_model()(
    #     uuid=weatherman_assistant_model_1_uuid
    # )

    # team = MultiAgentTeam(
    #     name="MultiAgentTeam",
    #     agent_1=agent_1,
    #     agent_2=agent_2,
    # )
    # await add_model(
    #     user_uuid=user_uuid,
    #     type_name="team",
    #     model_name=MultiAgentTeam.__name__,
    #     model_uuid=team_model_uuid,
    #     model=team.model_dump(),
    # )

    # # Then create autogen agents by monkeypatching create_autogen method
    # user_proxy_agent = autogen.agentchat.UserProxyAgent(
    #     "user_proxy",
    #     code_execution_config=False,
    # )

    # weatherman_agent_1 = autogen.agentchat.AssistantAgent(
    #     name="weather_man_1",
    #     system_message="You are the weather man. Ask the user to give you the name of a city and then provide the weather forecast for that city.",
    #     llm_config=llm_config,
    #     code_execution_config=False,
    # )

    # get_forecast_for_city_mock = MagicMock()

    # # @user_proxy_agent.register_for_execution()  # type: ignore [misc]
    # # @weatherman_agent_1.register_for_llm(
    # #     description="Get weather forecast for a city"
    # # )  # type: ignore [misc]
    # def get_forecast_for_city(city: str) -> str:
    #     get_forecast_for_city_mock(city)
    #     return f"The weather in {city} is sunny today."

    # async def weatherman_create_autogen(  # type: ignore [no-untyped-def]
    #     cls, model_id, user_id
    # ) -> autogen.agentchat.AssistantAgent:
    #     f_info = FunctionInfo(
    #         function=get_forecast_for_city,
    #         description="Get weather forecast for a city",
    #         name="get_forecast_for_city",
    #     )
    #     return weatherman_agent_1, [f_info]

    # async def user_proxy_create_autogen(  # type: ignore [no-untyped-def]
    #     cls, model_id, user_id
    # ) -> autogen.agentchat.UserProxyAgent:
    #     return user_proxy_agent, []

    # if enable_monkeypatch:
    #     monkeypatch.setattr(
    #         AssistantAgent, "create_autogen", weatherman_create_autogen
    #     )

    #     monkeypatch.setattr(
    #         UserProxyAgent, "create_autogen", user_proxy_create_autogen
    #     )

    # team = await MultiAgentTeam.create_autogen(
    #     model_id=uuid.UUID(team_model_uuid), user_id=uuid.UUID(user_uuid)
    # )

    # assert hasattr(team, "initiate_chat")

    # d = {"count": 0}

    # def input(prompt: str, d: Dict[str, int] = d) -> str:
    #     d["count"] += 1
    #     if d["count"] == 1:
    #         return f"[{datetime.now()}] What's the weather in New York today?"
    #     elif d["count"] == 2:
    #         return ""
    #     else:
    #         return "exit"

    # monkeypatch.setattr(IOConsole, "input", lambda self, prompt: input(prompt))

    # chat_result = team.initiate_chat(
    #     message="Hi! Tell me the city for which you want the weather forecast.",
    # )

    # last_message = chat_result.chat_history[-1]

    # if enable_monkeypatch:
    #     get_forecast_for_city_mock.assert_called_once_with("New York")
    #     # get_forecast_for_city_mock.assert_not_called()
    #     assert "sunny" in last_message["content"]
    # else:
    #     # assert "sunny" not in last_message["content"]
    #     # assert "weather" in last_message["content"]
    #     assert isinstance(last_message["content"], str)
