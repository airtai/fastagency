from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI

from ..workflow import wf

app = FastAgency(
    provider=wf,
    ui=MesopUI(),
    title="My FastAgency App Without Auth",
)

# start the fastagency app with the following command
# gunicorn my_fastagency_app_without_auth.deployment.main:app
