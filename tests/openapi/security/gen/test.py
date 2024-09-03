from main_gen import app, read_items_items__get

# apikeyheader_parameters = APIKeyHeaderParameterCls(value="super secret key", api_key_header=apikeyheader)
app.set_security("apikeyheader", "super secret key")

resp = read_items_items__get(city="New York", security=apikeyheader_parameters)
print(resp)
