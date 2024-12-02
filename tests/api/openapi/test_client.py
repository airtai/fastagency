from pathlib import Path

import pytest
from fastapi.params import Path as FastAPIPath
from fastapi.params import Query

from fastagency.api.openapi import OpenAPI


class TestOpenAPI:
    def test_simple_create_client(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        assert json_path.exists(), json_path.resolve()

        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json=openapi_json)

        assert client is not None
        assert isinstance(client, OpenAPI)

        assert client._servers == [
            {"url": "http://localhost:8080", "description": "Local environment"}
        ]

        assert len(client._registered_funcs) == 1, client._registered_funcs
        assert (
            client._registered_funcs[0].__name__
            == "update_item_items__item_id__ships__ship__put"
        )
        assert (
            client._registered_funcs[0].__doc__
            == """
    Update Item
    """
        )

        json2_path = Path(__file__).parent / "templates" / "openapi2.json"
        assert json2_path.exists(), json2_path.resolve()

        openapi2_json = json2_path.read_text()
        client2 = OpenAPI.create(openapi_json=openapi2_json)

        assert client2 is not None
        assert isinstance(client2, OpenAPI)

        assert len(client2._registered_funcs) == 3, client2._registered_funcs

        actual = [x.__name__ for x in client2._registered_funcs]
        expected = [
            "list_pets",
            "create_pets",
            "show_pet_by_id",
        ]
        assert actual == expected, actual

    def test_create_client_with_servers(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        assert json_path.exists(), json_path.resolve()

        servers = [
            {"url": "http://custom_server:8080", "description": "Local environment"}
        ]

        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json=openapi_json, servers=servers)

        assert client._servers == servers

    def test_get_functions(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json=openapi_json)

        function_names = client.function_names
        expected = ["update_item_items__item_id__ships__ship__put"]
        assert function_names == expected, function_names

        json2_path = Path(__file__).parent / "templates" / "openapi2.json"
        openapi2_json = json2_path.read_text()
        client2 = OpenAPI.create(openapi_json=openapi2_json)

        function_names2 = client2.function_names
        expected2 = ["list_pets", "create_pets", "show_pet_by_id"]
        assert function_names2 == expected2, function_names2

    def test_get_functions_to_register(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json=openapi_json)

        functions = client._get_functions_to_register(
            ["update_item_items__item_id__ships__ship__put"]
        )
        expected = ["update_item_items__item_id__ships__ship__put"]
        assert [f.__name__ for f in functions] == expected
        with pytest.raises(ValueError) as e:  # noqa: PT011
            client._get_functions_to_register(["func_does_not_exists"])
        assert (
            str(e.value)
            == f"Following functions {set(['func_does_not_exists'])} are not valid functions"  # noqa: C405
        ), str(e.value)

        json2_path = Path(__file__).parent / "templates" / "openapi2.json"
        openapi2_json = json2_path.read_text()
        client2 = OpenAPI.create(openapi_json=openapi2_json)

        functions2 = client2._get_functions_to_register(["list_pets"])
        expected2 = ["list_pets"]
        assert [f.__name__ for f in functions2] == expected2
        with pytest.raises(ValueError) as e:  # noqa: PT011
            client2._get_functions_to_register(["func_does_not_exists"])
        assert (
            str(e.value)
            == f"Following functions {set(['func_does_not_exists'])} are not valid functions"  # noqa: C405
        ), str(e.value)

    @pytest.mark.parametrize(
        ("input", "expected"),
        [
            ("/gif/{gifId}", "/gif/{gif_id}"),
            ("/gif/{GifId}", "/gif/{gif_id}"),
            ("/Gif/{GifId}", "/Gif/{gif_id}"),
            ("/Gif/{userId}/gif/{GifId}", "/Gif/{user_id}/gif/{gif_id}"),
        ],
    )
    def test_camel_to_snake_within_braces(self, input: str, expected: str) -> None:
        result = OpenAPI._convert_camel_case_within_braces_to_snake(input)

        assert result == expected, result

    def test_remove_pydantic_undefined_from_tools(self) -> None:
        tools = [
            {
                "type": "function",
                "function": {
                    "description": "Get GIFs for a topic.",
                    "name": "get_gifs_for_topic_gifs_get",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "default": Query(),
                                "description": "topic",
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "description": "Get GIF by Id.",
                    "name": "get_gif_by_id_gifs__gif_id__get",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "gif_id": {
                                "type": "integer",
                                "default": FastAPIPath(),
                                "description": "gif_id",
                            }
                        },
                        "required": [],
                    },
                },
            },
        ]
        result = OpenAPI._remove_pydantic_undefined_from_tools(tools)

        expected = [
            {
                "type": "function",
                "function": {
                    "description": "Get GIFs for a topic.",
                    "name": "get_gifs_for_topic_gifs_get",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "topic",
                            }
                        },
                        "required": ["topic"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "description": "Get GIF by Id.",
                    "name": "get_gif_by_id_gifs__gif_id__get",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "gif_id": {"type": "integer", "description": "gif_id"}
                        },
                        "required": ["gif_id"],
                    },
                },
            },
        ]
        assert result == expected, result
