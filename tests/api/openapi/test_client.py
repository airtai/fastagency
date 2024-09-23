from pathlib import Path

import pytest

from fastagency.api.openapi import OpenAPI


class TestOpenAPI:
    def test_simple_create_client(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        assert json_path.exists(), json_path.resolve()

        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json)

        assert client is not None
        assert isinstance(client, OpenAPI)

        assert len(client.registered_funcs) == 1, client.registered_funcs
        assert (
            client.registered_funcs[0].__name__
            == "update_item_items__item_id__ships__ship__put"
        )
        assert (
            client.registered_funcs[0].__doc__
            == """
    Update Item
    """
        )

        json2_path = Path(__file__).parent / "templates" / "openapi2.json"
        assert json2_path.exists(), json2_path.resolve()

        openapi2_json = json2_path.read_text()
        client2 = OpenAPI.create(openapi2_json)

        assert client2 is not None
        assert isinstance(client2, OpenAPI)

        assert len(client2.registered_funcs) == 3, client2.registered_funcs

        actual = [x.__name__ for x in client2.registered_funcs]
        expected = [
            "list_pets",
            "create_pets",
            "show_pet_by_id",
        ]
        assert actual == expected, actual

    def test_get_functions(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json)

        functions = client.get_functions()
        expected = ["update_item_items__item_id__ships__ship__put"]
        assert functions == expected, functions

        json2_path = Path(__file__).parent / "templates" / "openapi2.json"
        openapi2_json = json2_path.read_text()
        client2 = OpenAPI.create(openapi2_json)

        functions2 = client2.get_functions()
        expected2 = ["list_pets", "create_pets", "show_pet_by_id"]
        assert functions2 == expected2, functions2

    def test_get_functions_to_register(self) -> None:
        json_path = Path(__file__).parent / "templates" / "openapi.json"
        openapi_json = json_path.read_text()
        client = OpenAPI.create(openapi_json)

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
        client2 = OpenAPI.create(openapi2_json)

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
        result = OpenAPI._camel_to_snake_within_braces(input)

        assert result == expected, result
