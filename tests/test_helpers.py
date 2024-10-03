from fastagency.helpers import jsonify_string


def test() -> None:
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
