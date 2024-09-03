from main_gen import app, read_items_items__get

from fastagency.openapi.security import APIKeyHeader

app.set_security(APIKeyHeader.Parameters(value="super secret key"))
app.set_security(
    APIKeyHeader.Parameters(value="super secret key"), "read_items_items__get"
)

resp = read_items_items__get(city="New York")

print(resp)
