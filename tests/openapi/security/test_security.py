import contextlib
import json
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Iterator

import requests
import uvicorn

from fastagency.openapi.client import Client
from fastagency.openapi.security import APIKeyHeader

from .secure_app import app

PORT = 9999


class Server(uvicorn.Server):
    def install_signal_handlers(self) -> None:
        pass

    @contextlib.contextmanager
    def run_in_thread(self) -> Iterator[None]:
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def test_secure_app_openapi() -> None:
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
    server = Server(config=config)

    expected_openapi_json_path = Path(__file__).parent / "expected_openapi.json"
    with expected_openapi_json_path.open() as f:
        expected_openapi_json = json.load(f)

    with server.run_in_thread():
        resp = requests.get(f"http://localhost:{PORT}/openapi.json")
        assert resp.status_code == 200
        actual_openapi_json = resp.json()
        assert actual_openapi_json == expected_openapi_json


def test_generate_client() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        td = Path(temp_dir) / "gen"

        with Path("./openapi.json").open() as f:
            openapi_json = f.read()

        main_name = Client.generate_code(
            input_text=openapi_json,
            output_dir=td,
        )
        assert main_name == "main_gen"
        assert (td / "main_gen.py").exists()
        assert (td / "models_gen.py").exists()

        with (td / "main_gen.py").open() as f:
            actual_main_gen = f.readlines()[4:]

        with (td / "models_gen.py").open() as f:
            actual_models_gen = f.readlines()[4:]

        expected_main_gen_path = Path(__file__).parent / "expected_main_gen.py"
        with expected_main_gen_path.open() as f:
            expected_main_gen = f.readlines()[4:]

        expected_models_gen_path = Path(__file__).parent / "expected_models_gen.py"
        with expected_models_gen_path.open() as f:
            expected_models_gen = f.readlines()[4:]

        assert actual_main_gen == expected_main_gen
        assert actual_models_gen == expected_models_gen


def test_import_and_call_generate_client() -> None:
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
    server = Server(config=config)

    with tempfile.TemporaryDirectory() as temp_dir:
        td = Path(temp_dir) / "gen"

        with server.run_in_thread():
            resp = requests.get(f"http://localhost:{PORT}/openapi.json")
            assert resp.status_code == 200
            openapi_json = resp.json()

            main_name = Client.generate_code(
                input_text=json.dumps(openapi_json),
                output_dir=td,
            )
            assert main_name == "main_gen"

            sys.path.insert(1, str(td))

            from main_gen import app as generated_client_app
            from main_gen import read_items_items__get

            assert generated_client_app.security != {}, generated_client_app.security

            # set global security params for all methods
            # generated_client_app.set_security_params(APIKeyHeader.Parameters(value="super secret key"))

            # or set security params for a specific method
            generated_client_app.set_security_params(
                APIKeyHeader.Parameters(value="super secret key"),
                "read_items_items__get",
            )

            # no security params added to the signature of the method
            client_resp = read_items_items__get(city="New York")
            assert client_resp == {"is_authenticated": True}
