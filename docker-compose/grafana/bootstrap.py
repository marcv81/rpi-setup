import json
import os
import requests

username = "admin"
password = "admin"
server = "http://%s:%s@rpi.localnet:3000" % (username, password)


def iter_json_data(dir):
    """Iterates over the payload in JSON files in a directory."""
    for filename in os.listdir(dir):
        if not filename.endswith(".json"):
            continue
        filename = dir + "/" + filename
        print("Processing %s" % filename)
        with open(filename) as f:
            data = json.load(f)
        yield data


def show_status(response):
    """Prints a status line according to the HTTP response."""
    if response.status_code == 200:
        print("Done")
    else:
        data = json.loads(response.text)
        print("Error: %s" % data["message"])


def create_datasources():
    """Creates all the datasources with API calls."""
    url = "%s/api/datasources/" % server
    headers = {"Content-Type": "application/json"}
    for data in iter_json_data("datasources"):
        data = json.dumps(data)
        response = requests.post(url, headers=headers, data=data)
        show_status(response)


def create_dashboards():
    """Creates all the sabhoards with API calls."""
    url = "%s/api/dashboards/db" % server
    headers = {"Content-Type": "application/json"}
    for data in iter_json_data("dashboards"):
        del data["id"]
        data = {"dashboard": data}
        data = json.dumps(data)
        response = requests.post(url, headers=headers, data=data)
        show_status(response)


create_datasources()
create_dashboards()
