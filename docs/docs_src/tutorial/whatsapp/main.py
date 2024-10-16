import os
# from typing import Annotated, Any, Optional

# from autogen import register_function
# from autogen.agentchat import ConversableAgent

# from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyQuery
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

infobip_base_url = os.getenv("INFOBIP_BASE_URL", "")
servers=[{"url": infobip_base_url, "description": "API base URL"}]
try:
    whatsapp_api = OpenAPI(
        title="WhatsApp API",
        servers=servers,
    ).create(openapi_json=openapi_json)
    whatsapp_api_key = os.getenv("WHATSAPP_API_KEY", "")
    whatsapp_api.set_security_params(APIKeyQuery.Parameters(value=whatsapp_api_key))
except Exception as e:
    print(f"Error creating WhatsApp API: {e}")
