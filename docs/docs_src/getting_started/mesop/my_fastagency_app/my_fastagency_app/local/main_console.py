from fastagency import FastAgency
from fastagency.ui.console import ConsoleUI

from ..workflow import wf


app = FastAgency(
    provider=wf,
    ui=ConsoleUI(),
    title="My FastAgency App",
)
