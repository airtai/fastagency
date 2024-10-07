from os import environ

from fastagency.app import FastAgency
from fastagency.ui.mesop import MesopUI
from fastagency.ui.nats import NatsProvider

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

user: str = "faststream"
password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

wf = NatsProvider.Workflows(
    nats_url=environ.get("NATS_URL", None), user="faststream", password=password
)

ui = MesopUI()

app = FastAgency(wf=wf, ui=ui)

# start the provider with the following command
# gunicorn main_mesop:app --reload
