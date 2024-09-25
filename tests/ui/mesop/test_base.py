import sys

import pytest

from fastagency.app import FastAgency
from fastagency.base import TextMessage
from fastagency.runtime.autogen.base import AutoGenWorkflows

if sys.version_info >= (3, 10):
    from fastagency.ui.mesop.base import MesopUI

    class TestMesopUI:
        def test_mesop_init(self) -> None:
            mesop_ui = MesopUI()
            assert mesop_ui is not None
            assert mesop_ui._in_queue is not None
            assert mesop_ui._out_queue is not None

        def test_create(self) -> None:
            mesop_ui = MesopUI()
            with pytest.raises(RuntimeError, match="MesopUI has not been created yet."):
                MesopUI.get_created_instance()

            wf = AutoGenWorkflows()
            app = FastAgency(wf=wf, ui=mesop_ui)

            with mesop_ui.create(app, "import_string"):
                assert MesopUI.get_created_instance() == mesop_ui
                assert mesop_ui.app == app

        def test_mesop_mesage(self) -> None:
            mesop_ui = MesopUI()

            io_msg = TextMessage(
                sender="sender",
                recipient="recipient",
                body="message",
            )

            mesop_msg = mesop_ui._mesop_message(io_msg)
            assert mesop_msg.conversation == mesop_ui
            assert mesop_msg.io_message == io_msg
