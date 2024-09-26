from fastagency import FastAgency
from fastagency.new.base import FastAPIProvider
from fastagency.ui.mesop import MesopUI

provider = FastAPIProvider.Client(
    url="http://localhost:8000", dicovery_path="/fastagency/discovery"
)

app = FastAgency(provider=provider, ui=MesopUI())

# run with the following command:
# fastagency app run main_mesop:app
