import inspect
import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, cast

import mesop.labs as mel
import mesop.server.static_file_serving
import mesop.server.wsgi_app
from flask import Flask, Response
from mesop.runtime import runtime
from mesop.server.static_file_serving import (
    WEB_COMPONENTS_PATH_SEGMENT,
    noop,
    send_file_compressed,
)
from mesop.server.static_file_serving import (
    configure_static_file_serving as configure_static_file_serving_original,
)
from mesop.utils.validate import validate

from ...logging import get_logger

logger = get_logger(__name__)


def configure_static_file_serving(
    app: Flask,
    static_file_runfiles_base: str,
    livereload_script_url: Optional[str] = None,
    preprocess_request: Callable[[], None] = noop,
    disable_gzip_cache: bool = False,
    default_allowed_iframe_parents: str = "'self'",
) -> None:
    logger.info("Configuring static file serving with patched method")

    configure_static_file_serving_original(
        app=app,
        static_file_runfiles_base=static_file_runfiles_base,
        livereload_script_url=livereload_script_url,
        preprocess_request=preprocess_request,
        disable_gzip_cache=disable_gzip_cache,
        default_allowed_iframe_parents=default_allowed_iframe_parents,
    )

    @app.route(f"/{WEB_COMPONENTS_PATH_SEGMENT}/__fast_agency_internal__/<path:path>")  # type: ignore[misc]
    def serve_web_components_fast_agency(path: str) -> Response:
        logger.info(f"Serve web components fast agency: {path}")

        root = Path(__file__).parents[3].resolve()
        serving_path = f"{root}/{path}"

        return send_file_compressed(  # type: ignore[no-any-return]
            serving_path,
            disable_gzip_cache=disable_gzip_cache,
        )


C = TypeVar("C", bound=Callable[..., Any])


def format_filename(filename: str) -> str:
    if ".runfiles" in filename:
        # Handle Bazel case
        return filename.split(".runfiles", 1)[1]
    else:
        # Handle pip CLI case
        return os.path.relpath(filename, os.getcwd())  # noqa: PTH109


def web_component_patched(*, path: str, skip_validation: bool = False):  # type: ignore
    """A decorator for defining a web component.

    This decorator is used to define a web component. It takes a path to the
    JavaScript file of the web component and an optional parameter to skip
    validation. It then registers the JavaScript file in the runtime.

    Args:
        path: The path to the JavaScript file of the web component.
        skip_validation: If set to True, skips validation. Defaults to False.
    """
    runtime().check_register_web_component_is_valid()

    current_frame = inspect.currentframe()
    assert current_frame  # nosec
    previous_frame = current_frame.f_back
    assert previous_frame  # nosec
    caller_module_file = inspect.getfile(previous_frame)
    caller_module_dir = format_filename(
        os.path.dirname(os.path.abspath(caller_module_file))  # noqa: PTH120,PTH100
    )
    full_path = os.path.normpath(os.path.join(caller_module_dir, path))  # noqa: PTH118
    # if not full_path.startswith("/"):
    #     full_path = "/" + full_path

    # ToDo: propagate below fix to mesop repo
    # In Windows, above if section from original web_component function
    # creates a path which looks like "/\__fast_agency_internal__\javascript\wakeup_component.js"
    # Below three lines fixes this
    if not full_path.startswith(os.sep):
        full_path = os.sep + full_path

    js_module_path = full_path

    def component_wrapper(fn: C) -> C:
        validated_fn = fn if skip_validation else validate(fn)

        @wraps(fn)
        def wrapper(*args: Any, **kw_args: Any):  # type: ignore
            runtime().context().register_js_module(js_module_path)
            return validated_fn(*args, **kw_args)

        return cast(C, wrapper)

    return component_wrapper


logger.info("Patching static file serving in Mesop")
mesop.server.wsgi_app.configure_static_file_serving = configure_static_file_serving
mel.web_component = web_component_patched


@mel.web_component(path="/__fast_agency_internal__/javascript/wakeup_component.js")  # type: ignore[misc]
def wakeup_component(
    *,
    on_wakeup: Callable[[mel.WebEvent], Any],
    key: Optional[str] = None,
) -> Any:
    return mel.insert_web_component(
        name="wakeup-component",
        key=key,
        events={
            "wakeupEvent": on_wakeup,
        },
        properties={},
    )
