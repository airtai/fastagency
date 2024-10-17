from typing import Annotated, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, StringConstraints, constr

from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader


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

    app = OpenAPI(
        title="Infobip WHATSAPP OpenApi Specification",
        description="OpenApi Spec containing WHATSAPP public endpoints for Postman collection purposes.",
        contact={"name": "Infobip support", "email": "support@infobip.com"},
        version="1.0.195",
        servers=[{"url": "k24wk8.api.infobip.com"}],
    )

    @app.post(
        "/whatsapp/1/message/text",
        response_model=InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo,
        description="Send a text message to a single recipient. Text messages can only be successfully delivered, if the recipient has contacted the business within the last 24 hours, otherwise template message should be used.",
        tags=["Send WhatsApp Message"],
        security=[
            APIKeyHeader(name="Authorization"),
        ],
    )
    def channels_whatsapp_send_whatsapp_text_message(
        body: InfobipwhatsappstandaloneapiserviceOpenapiTextMessage,
    ) -> InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo:
        """Send WhatsApp text message."""
        return InfobipwhatsappstandaloneapiserviceOpenapiSingleMessageInfo()

    return app  # type: ignore[return-value]
