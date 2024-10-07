from pathlib import Path
from typing import Any, Callable, Optional

import mesop.labs as mel

pp = Path(__file__).parent
# os.path.dirname(__file__)
path_2_js = pp / "counter_component.js"
# path_2_js = os.path.join(pp, "counter_component.js")
# path_2_js = os.path.join(".", "counter_component.js")
# print("dir je:", pp, "u totalu:", path_2_js)


# @mel.web_component(path=path_2_js)
@mel.web_component(path="/javascript/counter_component.js")  # type: ignore[misc]
def counter_component(
    *,
    value: int,
    on_decrement: Callable[[mel.WebEvent], Any],
    key: Optional[str] = None,
) -> mel.WebComponent:
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
