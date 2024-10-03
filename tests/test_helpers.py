from fastagency.helpers import jsonify_string


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
