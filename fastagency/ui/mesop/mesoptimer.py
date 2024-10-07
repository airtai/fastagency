from pathlib import Path
from typing import Any, Callable, Optional

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

pp = Path(__file__).parent
# os.path.dirname(__file__)
path_2_js = pp / "counter_component.js"
# path_2_js = os.path.join(pp, "counter_component.js")
# path_2_js = os.path.join(".", "counter_component.js")
# print("dir je:", pp, "u totalu:", path_2_js)


def configure_static_file_serving(
    app: Flask,
    static_file_runfiles_base: str,
    livereload_script_url: Optional[str] = None,
    preprocess_request: Callable[[], None] = noop,
    disable_gzip_cache: bool = False,
    default_allowed_iframe_parents: str = "'self'",
) -> None:
    configure_static_file_serving_original(
        app=app,
        static_file_runfiles_base=static_file_runfiles_base,
        livereload_script_url=livereload_script_url,
        preprocess_request=preprocess_request,
        disable_gzip_cache=disable_gzip_cache,
        default_allowed_iframe_parents=default_allowed_iframe_parents,
    )

    @app.route(f"/{WEB_COMPONENTS_PATH_SEGMENT}/__fast_agency_internal__/<path:path>")
    def serve_web_components_fast_agency(path: str) -> Response:
        root = Path(__file__).parents[3].resolve()
        serving_path = f"{root}/{path}"

        return send_file_compressed(  # type: ignore[no-any-return]
            serving_path,
            disable_gzip_cache=disable_gzip_cache,
        )


mesop.server.wsgi_app.configure_static_file_serving = configure_static_file_serving


# @mel.web_component(path=path_2_js)
@mel.web_component(path="__fast_agency_internal__/javascript/counter_component.js")  # type: ignore[misc]
def counter_component(
    *,
    value: int,
    on_decrement: Callable[[mel.WebEvent], Any],
    key: Optional[str] = None,
) -> Any:
    return mel.insert_web_component(
        name="quickstart-counter-component",
        key=key,
        events={
            "decrementEvent": on_decrement,
        },
        properties={
            "value": value,
        },
    )
