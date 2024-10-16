import os
# from typing import Annotated, Any, Optional

# from autogen import register_function
# from autogen.agentchat import ConversableAgent

# from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
# from fastagency.runtimes.autogen.autogen import AutoGenWorkflows
# from fastagency.ui.mesop import MesopUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

with open("examples/openapi/whatsapp_openapi.json") as f:
    openapi_json = f.read()

# infobip_base_url = os.getenv("INFOBIP_BASE_URL", "")
whatsapp_api_key = os.getenv("WHATSAPP_API_KEY", "")

whatsapp_api = OpenAPI.create(openapi_json=openapi_json)
whatsapp_api.set_security_params(APIKeyHeader.Parameters(value=whatsapp_api_key))
