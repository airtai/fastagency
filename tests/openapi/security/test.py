from main_gen import read_items_items__get, APIKeyHeaderParameterCls, apikeyheader


apikeyheader_parameters = APIKeyHeaderParameterCls(value="super secret key", api_key_header=apikeyheader)

resp = read_items_items__get(city="New York", security=apikeyheader_parameters)
print(resp)
