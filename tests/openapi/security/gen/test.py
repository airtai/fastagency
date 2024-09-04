from main_gen import app, read_items_items__get

from fastagency.openapi.security import APIKeyHeader

assert app.security != {}, app.security

# set global security params for all methods
app.set_security_params(APIKeyHeader.Parameters(value="super secret key"))

# or set security params for a specific method
app.set_security_params(
    APIKeyHeader.Parameters(value="super secret key"), "read_items_items__get"
)

# no security params added to the signature of the method
resp = read_items_items__get(city="New York")

print(resp)  # noqa: T201
