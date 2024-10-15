from fastagency.api.openapi import OpenAPI

def configure_oauth_client(
    openapi_url: str, username: str, password: str
) -> OpenAPI:
    from fastagency.api.openapi import OpenAPI
    from fastagency.api.openapi.security import OAuth2PasswordBearer

    api_client = OpenAPI.create(openapi_url=openapi_url) # API openapi specification url
    api_client.set_security_params(
        OAuth2PasswordBearer.Parameters(
            username=username, # your API username
            password=password, # your API password
        )
    )

    return api_client

def configure_oauth_client_token(
    openapi_url: str, token: str
) -> OpenAPI:
    from fastagency.api.openapi import OpenAPI
    from fastagency.api.openapi.security import OAuth2PasswordBearer

    api_client = OpenAPI.create(openapi_url=openapi_url) # API openapi specification url
    api_client.set_security_params(OAuth2PasswordBearer.Parameters(bearer_token=token)) # API token

    return api_client

def configure_api_key_query_client(
    openapi_url: str, api_key: str
) -> OpenAPI:
    from fastagency.api.openapi import OpenAPI
    from fastagency.api.openapi.security import APIKeyQuery

    api_client = OpenAPI.create(openapi_url=openapi_url) # API openapi specification url
    api_client.set_security_params(APIKeyQuery.Parameters(value=api_key)) # API key

    return api_client

def configure_api_key_header_client(
    openapi_url: str, api_key: str
) -> OpenAPI:
    from fastagency.api.openapi import OpenAPI
    from fastagency.api.openapi.security import APIKeyHeader

    api_client = OpenAPI.create(openapi_url=openapi_url) # API openapi specification url
    api_client.set_security_params(APIKeyHeader.Parameters(value=api_key)) # API key

    return api_client

def configure_api_key_cookie_client(
    openapi_url: str, api_key: str
) -> OpenAPI:
    from fastagency.api.openapi import OpenAPI
    from fastagency.api.openapi.security import APIKeyCookie

    api_client = OpenAPI.create(openapi_url=openapi_url) # API openapi specification url
    api_client.set_security_params(APIKeyCookie.Parameters(value=api_key)) # API key

    return api_client

def configure_http_bearer_client(
    openapi_url: str, api_key: str
) -> OpenAPI:
    from fastagency.api.openapi import OpenAPI
    from fastagency.api.openapi.security import HTTPBearer

    api_client = OpenAPI.create(openapi_url=openapi_url) # API openapi specification url
    api_client.set_security_params(HTTPBearer.Parameters(value=api_key)) # API key

    return api_client
