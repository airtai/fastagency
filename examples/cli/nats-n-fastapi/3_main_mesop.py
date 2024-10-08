from os import environ

from fastagency.app import FastAgency
from fastagency.ui.fastapi import FastAPIAdapter
from fastagency.ui.mesop import MesopUI

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]
nats_url = nats_url.replace("nats://", "ws://")  # nosemgrep
nats_url = nats_url.replace("4222", "9222")

nats_user: str = "faststream"
nats_password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

fastapi_url = "http://localhost:8008"
fastapi_user: str = "fastapi"
fastapi_password: str = environ.get("FASTAPI_PASSWORD")  # type: ignore[assignment]

wf = FastAPIAdapter.create_provider(
    fastapi_url=fastapi_url,
    fastapi_user=fastapi_user,
    fastapi_password=fastapi_password,
    nats_url=nats_url,
    nats_user=nats_user,
    nats_password=nats_password,
)

ui = MesopUI()

app = FastAgency(provider=wf, ui=ui)

# write their own routes here
...

# start the provider with the following command
# gunicorn 3_main_mesop:app -b 0.0.0.0:8888 --reload
