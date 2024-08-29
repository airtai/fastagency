import importlib
import inspect
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
)

import requests
from fastapi_code_generator.__main__ import generate_code

from .fastapi_code_generator_helpers import patch_get_parameter_type

if TYPE_CHECKING:
    from autogen.agentchat import ConversableAgent

__all__ = ["Client"]

API_KEY_LOOKUP = {
    "APIKeyHeader": "X-Key",
}

def _get_api_key_header(api_key: inspect.Parameter) -> str:
    for key in API_KEY_LOOKUP:
        if key in api_key.annotation:
            return API_KEY_LOOKUP[key]
    raise ValueError(f"API key {api_key} not found in API_KEY_LOOKUP")

@contextmanager
def add_to_globals(new_globals: Dict[str, Any]) -> Iterator[None]:
    old_globals: Dict[str, Any] = {}
    try:
        for key, value in new_globals.items():
            if key in globals():
                old_globals[key] = globals()[key]
            globals()[key] = value
        yield
    finally:
        for key, value in old_globals.items():
            globals()[key] = value


class Client:
    def __init__(
        self, servers: List[Dict[str, Any]], title: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Proxy class to generate client from OpenAPI schema."""
        self.servers = servers
        self.title = title
        self.kwargs = kwargs
        self.registered_funcs: List[Callable[..., Any]] = []
        self.globals: Dict[str, Any] = {}

    @staticmethod
    def _get_params(
        path: str, func: Callable[..., Any]
    ) -> Tuple[Set[str], Set[str], Optional[str], Set[str]]:
        sig = inspect.signature(func)

        params_names = set(sig.parameters.keys())

        path_params = set(re.findall(r"\{(.+?)\}", path))
        if not path_params.issubset(params_names):
            raise ValueError(f"Path params {path_params} not in {params_names}")

        body = "body" if "body" in params_names else None

        security = None
        if "security" in params_names:
            security = _get_api_key_header(sig.parameters["security"])

        q_params = set(params_names) - path_params - {body} - {"security"}

        return q_params, path_params, body, security

    def _process_params(
        self, path: str, func: Callable[[Any], Any], **kwargs: Any
    ) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
        q_params, path_params, body, security = Client._get_params(path, func)

        expanded_path = path.format(**{p: kwargs[p] for p in path_params})

        url = self.servers[0]["url"] + expanded_path

        body_dict = (
            {
                "json": kwargs[body].model_dump()
                if hasattr(kwargs[body], "model_dump")
                else kwargs[body].dict()
            }
            if body and body in kwargs
            else {}
        )
        body_dict["headers"] = {"Content-Type": "application/json"}
        if security:
            body_dict["headers"][security] = kwargs["security"]

        params = {k: v for k, v in kwargs.items() if k in q_params}

        return url, params, body_dict

    def _request(
        self,
        method: Literal["put", "get", "post", "delete"],
        path: str,
        description: Optional[str] = None,
        **kwargs: Any,
    ) -> Callable[..., Dict[str, Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Dict[str, Any]]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
                url, params, body_dict = self._process_params(path, func, **kwargs)
                response = getattr(requests, method)(url, params=params, **body_dict)
                return response.json()  # type: ignore [no-any-return]

            wrapper._description = (  # type: ignore [attr-defined]
                description or func.__doc__.strip()
                if func.__doc__ is not None
                else None
            )

            self.registered_funcs.append(wrapper)

            return wrapper

        return decorator  # type: ignore [return-value]

    def put(self, path: str, **kwargs: Any) -> Callable[..., Dict[str, Any]]:
        return self._request("put", path, **kwargs)

    def get(self, path: str, **kwargs: Any) -> Callable[..., Dict[str, Any]]:
        return self._request("get", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Callable[..., Dict[str, Any]]:
        return self._request("post", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Callable[..., Dict[str, Any]]:
        return self._request("delete", path, **kwargs)

    @classmethod
    def _get_template_dir(cls) -> Path:
        path = Path(__file__).parents[2] / "templates"
        if not path.exists():
            raise RuntimeError(f"Template directory {path.resolve()} not found.")
        return path

    @classmethod
    def generate_code(
        cls,
        input_text: str,
        output_dir: Path,
        disable_timestamp: bool = False,
        custom_visitors: Optional[List[Path]] = None,
    ) -> str:
        with patch_get_parameter_type():
            generate_code(
                input_name="openapi.json",
                input_text=input_text,
                encoding="utf-8",
                output_dir=output_dir,
                template_dir=cls._get_template_dir(),
                disable_timestamp=disable_timestamp,
                custom_visitors=custom_visitors,
            )
            # Use unique file name for main.py
            main_name = f"main_{output_dir.name}"
            main_path = output_dir / f"{main_name}.py"
            shutil.move(output_dir / "main.py", main_path)

            # Change "from models import" to "from models_unique_name import"
            with open(main_path) as f:  # noqa: PTH123
                main_py_code = f.read()
            main_py_code = main_py_code.replace(
                "from .models import", f"from models_{output_dir.name} import"
            )
            with open(main_path, "w") as f:  # noqa: PTH123
                f.write(main_py_code)

            # Use unique file name for models.py
            models_name = f"models_{output_dir.name}"
            models_path = output_dir / f"{models_name}.py"
            shutil.move(output_dir / "models.py", models_path)

            return main_name

    def set_globals(self, main: ModuleType, sufix: str) -> None:
        xs = {k: v for k, v in main.__dict__.items() if not k.startswith("__")}
        self.globals = {
            k: v
            for k, v in xs.items()
            if hasattr(v, "__module__")
            and v.__module__ in [f"models_{sufix}", "typing"]
        }

    @classmethod
    def create(cls, openapi_json: str) -> "Client":
        with tempfile.TemporaryDirectory() as temp_dir:
            td = Path(temp_dir)
            sufix = td.name

            main_name = cls.generate_code(
                input_text=openapi_json,
                output_dir=td,
            )
            # add td to sys.path
            try:
                sys.path.append(str(td))
                main = importlib.import_module(main_name, package=td.name)  # nosemgrep
            finally:
                sys.path.remove(str(td))

            client: Client = main.app  # type: ignore [attr-defined]
            client.set_globals(main, sufix=sufix)

            return client

    def register_for_llm(self, agent: "ConversableAgent") -> None:
        with add_to_globals(self.globals):
            for f in self.registered_funcs:
                agent.register_for_llm()(f)

    def register_for_execution(self, agent: "ConversableAgent") -> None:
        for f in self.registered_funcs:
            agent.register_for_execution()(f)
