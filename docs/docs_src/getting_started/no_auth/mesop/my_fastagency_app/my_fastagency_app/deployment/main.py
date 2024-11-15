from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI

from ..workflow import wf

ui = MesopUI()


app = FastAgency(
    provider=wf,
    ui=ui,
    title="My FastAgency App",
)

# start the fastagency app with the following command
# gunicorn my_fastagency_app.deployment.main:app
