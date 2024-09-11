from pathlib import Path

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
