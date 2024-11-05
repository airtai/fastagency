from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI

from .workflow import wf


app = FastAgency(provider=wf, ui=MesopUI(), title="Learning Chat")
