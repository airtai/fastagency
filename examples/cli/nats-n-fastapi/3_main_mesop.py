from os import environ

from fastagency.app import FastAgency
from fastagency.ui.fastapi import FastAPIProvider
from fastagency.ui.mesop import MesopUI

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

user: str = "fastapi"
password: str = environ.get("FASTAPI_PASSWORD")  # type: ignore[assignment]

wf = FastAPIProvider.Workflows(
    fastapi_url=environ.get("FASTAPI_URL", None), user=user, password=password
)

ui = MesopUI()

app = FastAgency(wf=wf, ui=ui)

# write their own routes here
...

# start the provider with the following command
# gunicorn main_mesop:app --reload
