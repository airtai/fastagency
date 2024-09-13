import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import Any, Callable
from unittest.mock import MagicMock

# from autogen.agentchat import AssistantAgent, UserProxyAgent
import autogen
import pytest
from autogen.io.console import IOConsole
from fastapi import BackgroundTasks
from faststream.nats import TestNatsBroker
from pydantic import BaseModel

import fastagency.studio.io.ionats
from fastagency.studio.app import add_model
from fastagency.studio.io.ionats import (  # type: ignore [attr-defined]
    InputResponseModel,
    ServerResponseModel,
    broker,
    stream,
)
from fastagency.studio.models.agents.assistant import AssistantAgent
from fastagency.studio.models.agents.user_proxy import UserProxyAgent
from fastagency.studio.models.base import Model
from fastagency.studio.models.llms.azure import AzureOAI, AzureOAIAPIKey
from fastagency.studio.models.teams.two_agent_teams import TwoAgentTeam


def as_dict(model: BaseModel) -> dict[str, Any]:
    return json.loads(model.model_dump_json())  # type: ignore [no-any-return]


class TestAutogen:
    @pytest.mark.azure_oai
    def test_ioconsole(
        self,
        azure_gpt35_turbo_16k_llm_config: dict[str, Any],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        d = {"count": 0}

        def input(prompt: str, d: dict[str, int] = d) -> str:
            d["count"] += 1
            if d["count"] == 1:
                return f"[{datetime.now()}] What's the weather in New York today?"
            elif d["count"] == 2:
                return ""
            else:
                return "exit"

        monkeypatch.setattr(IOConsole, "input", lambda self, prompt: input(prompt))

        # print(f"{llm_config=}")

        weather_man = autogen.agentchat.AssistantAgent(
            name="weather_man",
            system_message="You are the weather man. Ask the user to give you the name of a city and then provide the weather forecast for that city.",
            llm_config=azure_gpt35_turbo_16k_llm_config,
            code_execution_config=False,
        )

        user_proxy = autogen.agentchat.UserProxyAgent(
            "user_proxy",
            code_execution_config=False,
        )

        get_forecast_for_city_mock = MagicMock()

        @user_proxy.register_for_execution()  # type: ignore [misc]
        @weather_man.register_for_llm(description="Get weather forecast for a city")  # type: ignore [misc]
        def get_forecast_for_city(city: str) -> str:
            get_forecast_for_city_mock(city)
            return f"The weather in {city} is sunny today."

        chat_result = weather_man.initiate_chat(
            recipient=user_proxy,
            message="Hi! Tell me the city for which you want the weather forecast.",
        )

        # print(f"{chat_result=}")

        last_message = chat_result.chat_history[-1]
        # print(f"{last_message=}")

        get_forecast_for_city_mock.assert_called_once_with("New York")
        assert "sunny" in last_message["content"]

    @pytest.mark.azure_oai
    @pytest.mark.nats
    @pytest.mark.asyncio
    async def test_ionats_success(  # noqa: C901
        self,
        azure_gpt35_turbo_16k_llm_config: dict[str, Any],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        user_id = uuid.uuid4()
        thread_id = uuid.uuid4()
        team_id = uuid.uuid4()

        azure_gpt35_turbo_16k_llm_config["temperature"] = 0.0

        ### begin sending inputs to server

        d = {"count": 0}

        def input(prompt: str, d: dict[str, int] = d) -> str:
            d["count"] += 1
            if d["count"] == 1:
                return f"[{datetime.now()}] What's the weather in New York today?"
            elif d["count"] == 2:
                return ""
            else:
                return "exit"

        actual = []
        terminate_chat_queue: asyncio.Queue = asyncio.Queue(maxsize=1)  # type: ignore [type-arg]

        @broker.subscriber(
            f"chat.client.messages.{user_id}.playground.{thread_id}", stream=stream
        )
        async def client_input_handler(msg: ServerResponseModel) -> None:
            if msg.type == "input":
                response = InputResponseModel(msg=input(msg.data.prompt))  # type: ignore [union-attr]

                await broker.publish(
                    response,
                    subject=f"chat.server.messages.{user_id}.playground.{thread_id}",
                )
            elif msg.type == "print":
                actual.append(msg.data.model_dump())
            elif msg.type == "terminate":
                await terminate_chat_queue.put(msg.data.model_dump())
            else:
                raise ValueError(f"Unknown message type {msg.type}")

        ### end sending inputs to server

        get_forecast_for_city_mock = MagicMock()

        async def create_team(
            team_id: uuid.UUID, user_id: uuid.UUID
        ) -> Callable[[str], list[dict[str, Any]]]:
            weather_man = autogen.agentchat.AssistantAgent(
                name="weather_man",
                system_message="You are the weather man. Ask the user to give you the name of a city and then provide the weather forecast for that city.",
                llm_config=azure_gpt35_turbo_16k_llm_config,
                code_execution_config=False,
            )

            user_proxy = autogen.agentchat.UserProxyAgent(
                "user_proxy",
                code_execution_config=False,
            )

            @user_proxy.register_for_execution()  # type: ignore [misc]
            @weather_man.register_for_llm(description="Get weather forecast for a city")  # type: ignore [misc]
            def get_forecast_for_city(city: str) -> str:
                get_forecast_for_city_mock(city)
                return f"The weather in {city} is sunny today."

            def initiate_chat(msg: str) -> list[dict[str, Any]]:
                chat_result: list[dict[str, Any]] = weather_man.initiate_chat(
                    recipient=user_proxy,
                    message="Hi! Tell me the city for which you want the weather forecast.",
                )
                return chat_result

            return initiate_chat

        monkeypatch.setattr(fastagency.studio.io.ionats, "create_team", create_team)

        async with TestNatsBroker(broker) as br:
            await br.publish(
                fastagency.studio.io.ionats.InitiateModel(
                    msg="exit",
                    thread_id=thread_id,
                    team_id=team_id,
                    user_id=user_id,
                ),
                subject="chat.server.initiate_chat",
            )

            expected = [
                {"msg": "(to user_proxy):\n\n"},
                {
                    "msg": "Hi! Tell me the city for which you want the weather forecast.\n"
                },
                {
                    "msg": "\n--------------------------------------------------------------------------------\n"
                },
                {"msg": "(to weather_man):\n\n"},
                {"msg": "What's the weather in New York today?\n"},
                {
                    "msg": "\n--------------------------------------------------------------------------------\n"
                },
                {"msg": "(to user_proxy):\n\n"},
                {"msg": " Suggested tool call (call_"},
                {"msg": 'Arguments: \n{\n  "city": "New York"\n}\n'},
                {
                    "msg": "*********************************************************************************"
                },
                {
                    "msg": "\n--------------------------------------------------------------------------------\n"
                },
                {"msg": ">>>>>>>> NO HUMAN INPUT RECEIVED."},
                {"msg": ">>>>>>>> USING AUTO REPLY..."},
                {"msg": ">>>>>>>> EXECUTING FUNCTION get_forecast_for_city..."},
                {"msg": "(to weather_man):\n\n"},
                {"msg": "(to weather_man):\n\n"},
                {"msg": " Response from calling tool (call_"},
                {"msg": "The weather in New York is sunny today.\n"},
                {
                    "msg": "*****************************************************************"
                },
                {
                    "msg": "\n--------------------------------------------------------------------------------\n"
                },
                {"msg": "(to user_proxy):\n\n"},
                {"msg": "The weather in New York today is sunny.\n"},
                {
                    "msg": "\n--------------------------------------------------------------------------------\n"
                },
            ]

            await asyncio.sleep(10)

            assert len(actual) == len(expected)
            for i in range(len(expected)):
                assert (
                    expected[i]["msg"] in actual[i]["msg"]
                ), f"{actual[i]} != {expected[i]}"

            result_set, _ = await asyncio.wait(
                (asyncio.create_task(terminate_chat_queue.get()),),
                timeout=30,
            )
            result = (result_set.pop()).result()
            assert result == {"msg": "Chat completed."}

    @pytest.mark.azure_oai
    @pytest.mark.nats
    @pytest.mark.asyncio
    async def test_ionats_error_msg(
        self,
        azure_gpt35_turbo_16k_llm_config: dict[str, Any],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        user_id = uuid.uuid4()
        thread_id = uuid.uuid4()
        team_id = uuid.uuid4()

        ### begin sending inputs to server

        d = {"count": 0}

        def input(prompt: str, d: dict[str, int] = d) -> str:
            d["count"] += 1
            if d["count"] == 1:
                return f"[{datetime.now()}] What's the weather in New York today?"
            elif d["count"] == 2:
                return ""
            else:
                return "exit"

        actual = []
        terminate_chat_queue: asyncio.Queue = asyncio.Queue(maxsize=1)  # type: ignore [type-arg]
        error_queue: asyncio.Queue = asyncio.Queue(maxsize=1)  # type: ignore [type-arg]

        @broker.subscriber(
            f"chat.client.messages.{user_id}.playground.{thread_id}", stream=stream
        )
        async def client_input_handler(msg: ServerResponseModel) -> None:
            if msg.type == "input":
                response = InputResponseModel(msg=input(msg.data.prompt))  # type: ignore [union-attr]

                await broker.publish(
                    response,
                    subject=f"chat.server.messages.{user_id}.playground.{thread_id}",
                )
            elif msg.type == "print":
                actual.append(msg.data.model_dump())
            elif msg.type == "terminate":
                await terminate_chat_queue.put(msg.data.model_dump())
            elif msg.type == "error":
                await error_queue.put(msg.data.model_dump())
            else:
                raise ValueError(f"Unknown message type {msg.type}")

        ### end sending inputs to server

        async def create_team(
            team_id: uuid.UUID, user_id: uuid.UUID
        ) -> Callable[[str], list[dict[str, Any]]]:
            raise ValueError("Triggering error in test")

        monkeypatch.setattr(fastagency.studio.io.ionats, "create_team", create_team)

        async with TestNatsBroker(broker) as br:
            await br.publish(
                fastagency.studio.io.ionats.InitiateModel(
                    msg="exit",
                    thread_id=thread_id,
                    team_id=team_id,
                    user_id=user_id,
                ),
                subject="chat.server.initiate_chat",
            )

            # await asyncio.sleep(10)

            result_set, _ = await asyncio.wait(
                (asyncio.create_task(error_queue.get()),),
                timeout=10,
            )
            result = (result_set.pop()).result()
            assert result == {"msg": "Triggering error in test"}

    @pytest.mark.azure_oai
    @pytest.mark.nats
    @pytest.mark.db
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "llm_model,api_key_model",  # noqa: PT006
        [
            (AzureOAI, AzureOAIAPIKey),
        ],
    )
    async def test_ionats_e2e(
        self,
        user_uuid: str,
        llm_model: Model,
        api_key_model: Model,
        # llm_config: Dict[str, Any],
        # monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        thread_id = uuid.uuid4()

        # Add secret, llm, agent, team to database
        api_key = api_key_model(  # type: ignore [operator]
            api_key=os.getenv("AZURE_OPENAI_API_KEY", default="*" * 64),
            name="api_key_model_name",
        )
        api_key_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="secret",
            model_name=f"{api_key_model.__name__}_test_ionats_e2e",  # type: ignore [attr-defined]
            model_uuid=api_key_model_uuid,
            model=api_key.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        llm = llm_model(  # type: ignore [operator]
            name="llm_model_name",
            model=os.getenv("AZURE_GPT35_MODEL", default="gpt-35-turbo-16k"),
            api_key=api_key.get_reference_model()(uuid=api_key_model_uuid),
            base_url=os.getenv(
                "AZURE_API_ENDPOINT", default="https://my-deployment.openai.azure.com"
            ),
            api_version=os.getenv("AZURE_API_VERSION", default="2024-02-01"),
        )
        llm_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="llm",
            model_name=llm_model.__name__,  # type: ignore [attr-defined]
            model_uuid=llm_model_uuid,
            model=llm.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        weatherman_assistant_model = AssistantAgent(
            llm=llm.get_reference_model()(uuid=llm_model_uuid),
            name="Assistant",
            system_message="test system message",
        )
        weatherman_assistant_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="agent",
            model_name=AssistantAgent.__name__,
            model_uuid=weatherman_assistant_model_uuid,
            model=weatherman_assistant_model.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        user_proxy_model = UserProxyAgent(
            name="UserProxyAgent",
            llm=llm.get_reference_model()(uuid=llm_model_uuid),
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

        team_model_uuid = str(uuid.uuid4())
        initial_agent = weatherman_assistant_model.get_reference_model()(
            uuid=weatherman_assistant_model_uuid
        )
        secondary_agent = user_proxy_model.get_reference_model()(
            uuid=user_proxy_model_uuid
        )
        team = TwoAgentTeam(
            name="TwoAgentTeam",
            initial_agent=initial_agent,
            secondary_agent=secondary_agent,
        )
        await add_model(
            user_uuid=user_uuid,
            type_name="team",
            model_name=TwoAgentTeam.__name__,
            model_uuid=team_model_uuid,
            model=team.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        ### begin sending inputs to server

        d = {"count": 0}

        def input(prompt: str, d: dict[str, int] = d) -> str:
            d["count"] += 1
            if d["count"] == 1:
                return f"[{datetime.now()}] What's the weather in New York today?"
            elif d["count"] == 2:
                return ""
            else:
                return "exit"

        actual = []
        terminate_chat_queue: asyncio.Queue = asyncio.Queue(maxsize=1)  # type: ignore [type-arg]

        @broker.subscriber(
            f"chat.client.messages.{user_uuid}.playground.{thread_id}", stream=stream
        )
        async def client_input_handler(msg: ServerResponseModel) -> None:
            if msg.type == "input":
                response = InputResponseModel(msg=input(msg.data.prompt))  # type: ignore [union-attr]

                await broker.publish(
                    response,
                    subject=f"chat.server.messages.{user_uuid}.playground.{thread_id}",
                )
            elif msg.type == "print":
                actual.append(msg.data.model_dump())
            elif msg.type == "terminate":
                await terminate_chat_queue.put(msg.data.model_dump())
            else:
                raise ValueError(f"Unknown message type {msg.type}")

        ### end sending inputs to server

        async with TestNatsBroker(broker) as br:
            await br.publish(
                fastagency.studio.io.ionats.InitiateModel(
                    msg="exit",
                    thread_id=thread_id,
                    team_id=team_model_uuid,
                    user_id=user_uuid,
                ),
                subject="chat.server.initiate_chat",
            )

            print(f"{actual=}")  # noqa

            assert isinstance(actual, list)

            result_set, _ = await asyncio.wait(
                (asyncio.create_task(terminate_chat_queue.get()),),
                timeout=30,
            )
            result = (result_set.pop()).result()
            assert result == {"msg": "Chat completed."}
