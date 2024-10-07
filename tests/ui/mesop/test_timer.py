from fastagency.ui.mesop.mesoptimer import get_counter_component

# def test_js_path():
#     assert js_path.exists()
#     assert js_path.is_file()


def test_get_counter_component() -> None:
    counter_component = get_counter_component()
    assert counter_component
