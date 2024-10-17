from typing import Annotated, Any, Optional

import pytest
from autogen import ConversableAgent, UserProxyAgent
from fastapi import FastAPI
from pydantic import BaseModel, Field, StringConstraints, constr

from fastagency.api.openapi.client import OpenAPI

# from fastagency.api.openapi.security import APIKeyHeader


def create_whatsapp_fastapi_app(host: str, port: int) -> FastAPI:
    class InfobipwhatsappstandaloneapiserviceOpenapiTextContent(BaseModel):
        text: constr(min_length=1, max_length=4096) = Field(  # type: ignore[valid-type]
            ..., description="Text of the message that will be sent."
        )
        previewUrl: Optional[bool] = Field(  # noqa: N815
            None,
            description="Allows for URL previews in text messages. If the value is set to `true`, text is expected to contain URL starting with `https://` or `http://`. The default value is `false`.",
        )

    class InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageStatus(BaseModel):
        groupId: Optional[int] = Field(  # noqa: N815
            None, description="Status group ID.", examples=[1]
        )
        groupName: Optional[str] = Field(  # noqa: N815
            None, description="Status group name.", examples=["PENDING"]
        )
        id: Optional[int] = Field(None, description="Status ID.", examples=[7])
        name: Optional[str] = Field(
            None, description="Status name.", examples=["PENDING_ENROUTE"]
        )
        description: Optional[str] = Field(
            None,
            description="Human-readable description of the status.",
            examples=["Message sent to next instance"],
        )
        action: Optional[str] = Field(
            None, description="Action that should be taken to eliminate the error."
        )

    class InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo(BaseModel):
        to: Optional[str] = Field(
            None, description="Message destination.", examples=["385977666618"]
        )
        messageCount: Optional[int] = Field(  # noqa: N815
            None, description="Number of messages required to deliver.", examples=[1]
        )
        messageId: Optional[str] = Field(  # noqa: N815
            None,
            description="The ID that uniquely identifies the message sent.",
            examples=["06df139a-7eb5-4a6e-902e-40e892210455"],
        )
        status: Optional[
            InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageStatus
        ] = None

    class InfobipwhatsappstandaloneapiserviceOpenapiTextMessage(BaseModel):
        from_: constr(min_length=1, max_length=24) = Field(  # type: ignore[valid-type]
            ...,
            alias="from",
            description="Registered WhatsApp sender number. Must be in international format.",
        )
        to: constr(min_length=1, max_length=24) = Field(  # type: ignore[valid-type]
            ...,
            description="Message recipient number. Must be in international format.",
        )
        messageId: Annotated[  # noqa: N815
            Optional[str], StringConstraints(min_length=0, max_length=50)  # type: ignore
        ] = Field(None, description="The ID that uniquely identifies the message sent.")
        content: InfobipwhatsappstandaloneapiserviceOpenapiTextContent
        callbackData: Annotated[  # noqa: N815
            Optional[str], StringConstraints(min_length=0, max_length=4000)
        ] = Field(
            None,
            description="Custom client data that will be included in Delivery Report.",
        )

    # app = OpenAPI(
    #     title="Infobip WHATSAPP OpenApi Specification",
    #     description="OpenApi Spec containing WHATSAPP public endpoints for Postman collection purposes.",
    #     contact={"name": "Infobip support", "email": "support@infobip.com"},
    #     version="1.0.195",
    #     servers=[{"url": "k24wk8.api.infobip.com"}],
    # )
    app = FastAPI(
        title="WhatsApp",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    @app.post(
        "/whatsapp/1/message/text",
        response_model=InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo,
        description="Send a text message to a single recipient. Text messages can only be successfully delivered, if the recipient has contacted the business within the last 24 hours, otherwise template message should be used.",
        tags=["Send WhatsApp Message"],
        # security=[
        #     APIKeyHeader(name="Authorization"),
        # ],
    )
    def send(
        body: InfobipwhatsappstandaloneapiserviceOpenapiTextMessage,
    ) -> InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo:
        """Send WhatsApp text message."""
        return InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo(
            to=body.to,
            messageCount=1,
        )

    return app


@pytest.fixture
def openapi_schema() -> dict[str, Any]:
    app = create_whatsapp_fastapi_app(host="127.0.0.1", port=8000)

    return app.openapi()


def test_openapi_schema(openapi_schema: dict[str, Any]) -> None:
    expected_schema = {
        "openapi": "3.1.0",
        "info": {"title": "WhatsApp", "version": "0.1.0"},
        "servers": [
            {"url": "http://127.0.0.1:8000", "description": "Local development server"}
        ],
        "paths": {
            "/whatsapp/1/message/text": {
                "post": {
                    "tags": ["Send WhatsApp Message"],
                    "summary": "Send",
                    "description": "Send a text message to a single recipient. Text messages can only be successfully delivered, if the recipient has contacted the business within the last 24 hours, otherwise template message should be used.",
                    "operationId": "send_whatsapp_1_message_text_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/InfobipwhatsappstandaloneapiserviceOpenapiTextMessage"
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo"
                                    }
                                }
                            },
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo": {
                    "properties": {
                        "to": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "To",
                            "description": "Message destination.",
                            "examples": ["385977666618"],
                        },
                        "messageCount": {
                            "anyOf": [{"type": "integer"}, {"type": "null"}],
                            "title": "Messagecount",
                            "description": "Number of messages required to deliver.",
                            "examples": [1],
                        },
                        "messageId": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Messageid",
                            "description": "The ID that uniquely identifies the message sent.",
                            "examples": ["06df139a-7eb5-4a6e-902e-40e892210455"],
                        },
                        "status": {
                            "anyOf": [
                                {
                                    "$ref": "#/components/schemas/InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageStatus"
                                },
                                {"type": "null"},
                            ]
                        },
                    },
                    "type": "object",
                    "title": "InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo",
                },
                "InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageStatus": {
                    "properties": {
                        "groupId": {
                            "anyOf": [{"type": "integer"}, {"type": "null"}],
                            "title": "Groupid",
                            "description": "Status group ID.",
                            "examples": [1],
                        },
                        "groupName": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Groupname",
                            "description": "Status group name.",
                            "examples": ["PENDING"],
                        },
                        "id": {
                            "anyOf": [{"type": "integer"}, {"type": "null"}],
                            "title": "Id",
                            "description": "Status ID.",
                            "examples": [7],
                        },
                        "name": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Name",
                            "description": "Status name.",
                            "examples": ["PENDING_ENROUTE"],
                        },
                        "description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Description",
                            "description": "Human-readable description of the status.",
                            "examples": ["Message sent to next instance"],
                        },
                        "action": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Action",
                            "description": "Action that should be taken to eliminate the error.",
                        },
                    },
                    "type": "object",
                    "title": "InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageStatus",
                },
                "InfobipwhatsappstandaloneapiserviceOpenapiTextContent": {
                    "properties": {
                        "text": {
                            "type": "string",
                            "maxLength": 4096,
                            "minLength": 1,
                            "title": "Text",
                            "description": "Text of the message that will be sent.",
                        },
                        "previewUrl": {
                            "anyOf": [{"type": "boolean"}, {"type": "null"}],
                            "title": "Previewurl",
                            "description": "Allows for URL previews in text messages. If the value is set to `true`, text is expected to contain URL starting with `https://` or `http://`. The default value is `false`.",
                        },
                    },
                    "type": "object",
                    "required": ["text"],
                    "title": "InfobipwhatsappstandaloneapiserviceOpenapiTextContent",
                },
                "InfobipwhatsappstandaloneapiserviceOpenapiTextMessage": {
                    "properties": {
                        "from": {
                            "type": "string",
                            "maxLength": 24,
                            "minLength": 1,
                            "title": "From",
                            "description": "Registered WhatsApp sender number. Must be in international format.",
                        },
                        "to": {
                            "type": "string",
                            "maxLength": 24,
                            "minLength": 1,
                            "title": "To",
                            "description": "Message recipient number. Must be in international format.",
                        },
                        "messageId": {
                            "anyOf": [
                                {"type": "string", "maxLength": 50, "minLength": 0},
                                {"type": "null"},
                            ],
                            "title": "Messageid",
                            "description": "The ID that uniquely identifies the message sent.",
                        },
                        "content": {
                            "$ref": "#/components/schemas/InfobipwhatsappstandaloneapiserviceOpenapiTextContent"
                        },
                        "callbackData": {
                            "anyOf": [
                                {"type": "string", "maxLength": 4000, "minLength": 0},
                                {"type": "null"},
                            ],
                            "title": "Callbackdata",
                            "description": "Custom client data that will be included in Delivery Report.",
                        },
                    },
                    "type": "object",
                    "required": ["from", "to", "content"],
                    "title": "InfobipwhatsappstandaloneapiserviceOpenapiTextMessage",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            }
        },
    }
    assert openapi_schema == expected_schema, openapi_schema


@pytest.mark.azure_oai
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_whatsapp_fastapi_app)],
    indirect=["fastapi_openapi_url"],
)
def test_end2end(
    fastapi_openapi_url: str,
    azure_gpt35_turbo_16k_llm_config: dict[str, Any],
) -> None:
    api = OpenAPI.create(openapi_url=fastapi_openapi_url)

    agent = ConversableAgent(name="agent", llm_config=azure_gpt35_turbo_16k_llm_config)
    user_proxy = UserProxyAgent(
        name="user_proxy",
        llm_config=azure_gpt35_turbo_16k_llm_config,
        human_input_mode="NEVER",
    )

    api._register_for_llm(agent)
    api._register_for_execution(user_proxy)

    message = (
        "I need to send a 'Hello, World!' from number 3378378333 to number 385911425425"
    )
    user_proxy.initiate_chat(
        agent,
        message=message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    message_existed = False
    expected_message = (
        '{"to": "385911425425", "messageCount": 1, "messageId": null, "status": null}'
    )
    for message in agent.chat_messages[user_proxy]:
        if (
            isinstance(message, dict)
            and "content" in message
            and isinstance(message["content"], str)
            and message["content"] == expected_message
        ):
            message_existed = True
            break
    assert message_existed, f"Expected message not found: {expected_message}"
