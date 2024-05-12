import csv
import requests
import urllib.request
import json
import pandas as pd
from flask import current_app
from datetime import datetime, timedelta

def main():
    # Configure the API URL and parameters
    base_url = "https://data.gov.au/data/api/3/action/datastore_search"
    resource_id = "d54f7465-74b8-4fff-8653-37e724d0ebbb"
    year = "2023"
    limit = 100000

    # Construct the API URL with the configured parameters
    api_url = f"{base_url}?resource_id={resource_id}&q={year}&limit={limit}"

    # Send a GET request to the API URL and retrieve the data as JSON
    data = requests.get(api_url).json()
    current_app.logger.info("Getting information as JSON")

    # Post the retrieved data to the Fission router for enqueueing
    requests.post(url='http://router.fission/enqueue/traffic_accidents',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(data)
                  )
    return 'OK'