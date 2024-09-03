from pathlib import Path

from fastagency.openapi.client import Client

# with tempfile.TemporaryDirectory() as temp_dir:
td = Path("./gen")
sufix = td.name
print(td.absolute())

with open("openapi.json") as f:
    openapi_json = f.read()

main_name = Client.generate_code(
    input_text=openapi_json,
    output_dir=td,
    # custom_visitors=[Path("./custom_visitor.py")]
)
print(main_name)
