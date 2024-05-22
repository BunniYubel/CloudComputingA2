import csv
import requests
import urllib.request
import json
import pandas as pd

api_url = "https://data.gov.au/data/api/3/action/datastore_search?resource_id=d54f7465-74b8-4fff-8653-37e724d0ebbb&q=2023&limit=100000"

data = requests.get(api_url).json()
print("Getting information as JSON")

requests.post(url='http://router.fission/enqueue/traffic_accidents',
              headers={'Content-Type': 'application/json'},
              data=json.dumps(data)
              )
