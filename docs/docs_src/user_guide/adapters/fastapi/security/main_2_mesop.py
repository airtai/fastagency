from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.app import FastAgency
from fastagency.ui.mesop import MesopUI

from fastagency.api.openapi.security import OAuth2PasswordBearer

fastapi_url = "http://localhost:8008"

# todo: add security params
# get token from /login route and pass token to provider

provider = FastAPIAdapter.create_provider(
    fastapi_url=fastapi_url,
)

# provider.set_security_params(
#     OAuth2PasswordBearer.Parameters(
#         username="user",
#         password="password" # pragma: allowlist secret
#     )
# )

app = FastAgency(
    provider=provider,
    ui=MesopUI(),
)

# start the provider with the following command
# gunicorn main_2_mesop:app -b 0.0.0.0:8888 --reload
