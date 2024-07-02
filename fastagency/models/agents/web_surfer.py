from typing import Annotated, Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID

from autogen.agentchat import Agent as AutogenAgent
from autogen.agentchat import AssistantAgent as AutogenAssistantAgent
from autogen.agentchat.contrib.web_surfer import WebSurferAgent as AutogenWebSurferAgent
from autogen.oai.client import OpenAIWrapper as AutogenOpenAIWrapper
from pydantic import Field
from typing_extensions import TypeAlias

from ...openapi.client import Client
from ..base import Model
from ..registry import register
from .base import AgentBaseModel, llm_type_refs

_org_generate_surfer_reply: Optional[Callable[..., Any]] = None


def _patch_generate_surfer_reply() -> None:
    global _org_generate_surfer_reply

    if _org_generate_surfer_reply is None:
        _org_generate_surfer_reply = AutogenWebSurferAgent.generate_surfer_reply

    def generate_surfer_reply(
        self: AutogenWebSurferAgent,
        messages: Optional[List[Dict[str, str]]] = None,
        sender: Optional[AutogenAgent] = None,
        config: Optional[AutogenOpenAIWrapper] = None,
    ) -> Tuple[bool, Optional[Union[str, Dict[str, str]]]]:
        global _org_generate_surfer_reply

        if messages is not None and "tool_responses" in messages[-1]:
            messages = messages.copy()
            messages.append(messages[-1].copy())
            messages[-1].pop("tool_responses")

        return _org_generate_surfer_reply(self, messages, sender, config)  # type: ignore[no-any-return]

    AutogenWebSurferAgent.generate_surfer_reply = generate_surfer_reply


_patch_generate_surfer_reply()


@register("secret")
class BingAPIKey(Model):
    api_key: Annotated[str, Field(description="The API Key from Bing")]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model = await cls.from_db(model_id)

        return my_model.api_key


BingAPIKeyRef: TypeAlias = BingAPIKey.get_reference_model()  # type: ignore[valid-type]


@register("agent")
class WebSurferAgent(AgentBaseModel):
    summarizer_llm: Annotated[
        llm_type_refs,
        Field(
            title="Summarizer LLM",
            description="This LLM will be used to generated summary of all pages visited",
        ),
    ]
    viewport_size: Annotated[
        int, Field(description="The viewport size of the browser")
    ] = 1080
    bing_api_key: Annotated[
        Optional[BingAPIKeyRef], Field(description="The Bing API key for the browser")
    ] = None

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> Tuple[AutogenAssistantAgent, List[Client]]:
        my_model = await cls.from_db(model_id)

        llm_model = await my_model.llm.get_data_model().from_db(my_model.llm.uuid)

        llm = await llm_model.create_autogen(my_model.llm.uuid, user_id)

        clients = await my_model.get_clients_from_toolboxes(user_id)  # noqa: F841

        summarizer_llm_model = await my_model.summarizer_llm.get_data_model().from_db(
            my_model.summarizer_llm.uuid
        )

        summarizer_llm = await summarizer_llm_model.create_autogen(
            my_model.summarizer_llm.uuid, user_id
        )

        bing_api_key = None
        if my_model.bing_api_key:
            bing_api_key_model = await my_model.bing_api_key.get_data_model().from_db(
                my_model.bing_api_key.uuid
            )
            bing_api_key = await bing_api_key_model.create_autogen(
                my_model.bing_api_key.uuid, user_id
            )

        browser_config = {
            "viewport_size": my_model.viewport_size,
            "bing_api_key": bing_api_key,
        }
        agent_name = my_model.name

        agent = AutogenWebSurferAgent(
            name=agent_name,
            llm_config=llm,
            summarizer_llm_config=summarizer_llm,
            browser_config=browser_config,
            **kwargs,
        )

        return agent, []
