from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI

from ..workflow import wf

app = FastAgency(
    provider=wf,
    ui=MesopUI(),
    title="My Bank App",
)

# start the fastagency app with the following command
# gunicorn my_bank_app.local.main_mesop:app
