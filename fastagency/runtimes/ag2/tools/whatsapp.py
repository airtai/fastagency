from typing import Union

from autogen import ConversableAgent

from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.ag2.ag2 import Toolable

WHATSAPP_OPENAPI_URL = "https://dev.infobip.com/openapi/products/whatsapp.json"
WHATSAPP_API_SERVER = "https://api.infobip.com"
WHATSAPP_FUNCTIONS = ["send_whatsapp_text_message"]


class WhatsAppTool(Toolable):
    def __init__(
        self,
        whatsapp_api_key: str,
        whatsapp_openapi_url: str = WHATSAPP_OPENAPI_URL,
        whatsapp_api_server: str = WHATSAPP_API_SERVER,
    ):
        """Create a new WhatsAppTool instance.

        Args:
            whatsapp_api_key (str): The WhatsApp API key.
            whatsapp_openapi_url (str): Url of the openapi schema for Infobip WhatsApp API, defaults to https://dev.infobip.com/openapi/products/whatsapp.json
            whatsapp_api_server (str): Url of the Infobip WhatsApp API server, defaults to https://api.infobip.com
        """
        self.whatsapp_api = OpenAPI.create(
            openapi_url=whatsapp_openapi_url,
            servers=[{"url": whatsapp_api_server}],
        )

        header_authorization = f"App {whatsapp_api_key}"
        self.whatsapp_api.set_security_params(
            APIKeyHeader.Parameters(value=header_authorization)
        )

    def register(
        self,
        *,
        caller: ConversableAgent,
        executor: Union[ConversableAgent, list[ConversableAgent]],
    ) -> None:
        executors = executor if isinstance(executor, list) else [executor]

        self.whatsapp_api._register_for_llm(caller, functions=WHATSAPP_FUNCTIONS)

        for executor in executors:
            self.whatsapp_api._register_for_execution(
                executor, functions=WHATSAPP_FUNCTIONS
            )
