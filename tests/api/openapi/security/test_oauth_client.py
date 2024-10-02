import json

from fastagency.api.openapi import OpenAPI


def test_generate_oauth2_client() -> None:
    schema = {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "servers": [
            {
                "url": "https://airt-chatbots-gecwdgakcse7g9bz.westeurope-01.azurewebsites.net/",
                "production": "Production environment",
            }
        ],
        "paths": {
            "/low": {
                "post": {
                    "summary": "Low Level",
                    "operationId": "low_level_low_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Message"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "title": "Response Low Level Low Post",
                                    }
                                }
                            },
                        }
                    },
                    "security": [{"OAuth2PasswordBearer": []}],
                }
            }
        },
        "components": {
            "schemas": {
                "Message": {
                    "properties": {
                        "role": {"type": "string", "title": "Role", "default": "user"},
                        "content": {"type": "string", "title": "Content"},
                    },
                    "type": "object",
                    "required": ["content"],
                    "title": "Message",
                }
            },
            "securitySchemes": {
                "OAuth2PasswordBearer": {
                    "type": "oauth2",
                    "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                }
            },
        },
    }

    OpenAPI.create(openapi_json=json.dumps(schema))
