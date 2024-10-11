from os import environ

from fastagency.adapters.nats import NatsAdapter
from fastagency.app import FastAgency
from fastagency.ui.mesop.mesop import MesopUI

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

fastapi_user: str = "fastapi"
fastapi_password: str = environ.get("FASTAPI_PASSWORD")  # type: ignore[assignment]

nats_user: str = "faststream"
nats_password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

provider = NatsAdapter.create_provider(
    nats_url=environ.get("NATS_URL", None), user=nats_user, password=nats_password
)

ui = MesopUI()

app = FastAgency(provider=provider, ui=ui)

# start the provider with the following command
# gunicorn 2_main_mesop:app -b 0.0.0.0:8888 --reload
