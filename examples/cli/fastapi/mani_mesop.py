from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI

provider = FastAPIProvider.Client(
    url="http://localhost:8000",
)

app = FastAgency(provider=provider, ui=MesopUI())

# run with the following command:
# fastagency ui run main_mesop:app
