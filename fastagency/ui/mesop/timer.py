import os
import os.path
import platform
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Optional, SupportsIndex

import mesop.labs as mel
import mesop.server.static_file_serving
import mesop.server.wsgi_app
from flask import Flask, Response
from mesop.server.static_file_serving import (
    WEB_COMPONENTS_PATH_SEGMENT,
    noop,
    send_file_compressed,
)
from mesop.server.static_file_serving import (
    configure_static_file_serving as configure_static_file_serving_original,
)

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


logger.info("Patching static file serving in Mesop")
mesop.server.wsgi_app.configure_static_file_serving = configure_static_file_serving


MEL_WEB_COMPONENT_PATH = "/__fast_agency_internal__/javascript/wakeup_component.js"
WINDOWS_MEL_WEB_COMPONENT_PATH = MEL_WEB_COMPONENT_PATH.replace("/", "\\")


# Extended subclass
class MyStr(str):
    def startswith(
        self,
        prefix: str | tuple[str, ...],  # type: ignore
        start: SupportsIndex | None = None,  # type: ignore
        end: SupportsIndex | None = None,  # type: ignore
    ) -> bool:
        if (
            platform.system() == "Windows"
            and self == WINDOWS_MEL_WEB_COMPONENT_PATH
            and prefix == "/"
        ):
            return True
        return super().startswith(prefix, start, end)


original_os_path_normpath = os.path.normpath


def os_path_normpath_patch(path: str) -> str:
    path = original_os_path_normpath(path)
    if path == WINDOWS_MEL_WEB_COMPONENT_PATH:
        return MyStr(path)
    return path


@contextmanager
def patch_os_and_str() -> Iterator[None]:
    os.path.normpath = os_path_normpath_patch  # type: ignore[assignment]
    yield
    os.path.normpath = original_os_path_normpath


def wakeup_component(
    *,
    on_wakeup: Callable[[mel.WebEvent], Any],
    key: Optional[str] = None,
) -> Any:
    with patch_os_and_str():

        @mel.web_component(path=MEL_WEB_COMPONENT_PATH)  # type: ignore[misc]
        def mel_wakeup_component(
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

        return mel_wakeup_component(on_wakeup=on_wakeup, key=key)
