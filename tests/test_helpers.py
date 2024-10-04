from pathlib import Path

from fastagency.helpers import jsonify_string, optional_temp_path


def test_hello() -> None:
    demo_text = """Hello, {"a": {"b": "c"}}   is some json data, but also {"c": [1,2,3]} is too"""
    expected = """Hello,
```
{
    "a": {
        "b": "c"
    }
}
```
is some json data, but also
```
{
    "c": [
        1,
        2,
        3
    ]
}
```
is too"""
    actual = jsonify_string(demo_text)
    assert actual == expected, actual


def test_bad_suggested_function_call() -> None:
    content = "**function_name**: `search_gifs`<br>\n**call_id**: `call_T70PONfhtAqCu6FdRWp1frAS`<br>\n**arguments**: {'q': 'cats', 'limit': 5}\n"
    expected = """**function_name**: `search_gifs`<br>
**call_id**: `call_T70PONfhtAqCu6FdRWp1frAS`<br>
**arguments**:{'q': 'cats', 'limit': 5}
"""
    actual = jsonify_string(content)
    assert actual == expected, actual


def test_optional_temp_path() -> None:
    with optional_temp_path() as temp_path:
        assert temp_path.exists()
    assert not temp_path.exists()

    with optional_temp_path(path="defined_path") as temp_path:
        assert temp_path == Path("defined_path")
