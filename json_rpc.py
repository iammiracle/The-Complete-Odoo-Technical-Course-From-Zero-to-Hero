import json
import random
import urllib.request

odoo_url = 'http://localhost:8069'
username = 'admin'
password = 'admin'
db = 'theodooguys'


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000)
    }
    headers = {
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers=headers)

    response = json.loads(urllib.request.urlopen(req).read().decode("UTF-8"))

    if response.get('error'):
        raise Exception(response["error"])
    return response["result"]


def call(url, service, method, *args):
    return json_rpc(f"{url}/jsonrpc", "call", {"service": service, "method": method, "args": args})


user_id = call(odoo_url, "common", "login", db, username, password)

print(user_id)

vals = {
    "name": "Property from JSON",
    "sales_id": 6
}

# create_property = call(odoo_url, "object", "execute", db, user_id, password, 'estate.property', 'create', vals)
# print(create_property)

read_property = call(odoo_url, "object", "execute", db, user_id, password, 'estate.property', 'read', [9])
print(read_property)