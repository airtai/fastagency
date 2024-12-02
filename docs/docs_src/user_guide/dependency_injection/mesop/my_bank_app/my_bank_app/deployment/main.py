from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI

from ..workflow import wf

ui = MesopUI()


app = FastAgency(
    provider=wf,
    ui=ui,
    title="My Bank App",
)

# start the fastagency app with the following command
# gunicorn my_bank_app.deployment.main:app
