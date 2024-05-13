import csv
import requests
import urllib.request
import json,logging
import pandas as pd
from flask import current_app
from datetime import datetime, timedelta

def main():
    #Version control purpose
    current_app.logger.info(f"Function last updated at: {datetime.datetime.now()}")
    
    # Configure the API URL and parameters
    base_url = "https://data.gov.au/data/api/3/action/datastore_search"
    resource_id = "d54f7465-74b8-4fff-8653-37e724d0ebbb"
    year = "2023"
    limit = 100000

    # Construct the API URL with the configured parameters
    api_url = f"{base_url}?resource_id={resource_id}&q={year}&limit={limit}"

    # Send a GET request to the API URL and retrieve the data as JSON
    try:
        data = requests.get(api_url).json()
        current_app.logger.info("Getting information as JSON")
        current_app.logger.info(f"Data retrieved: {data}")
    except Exception as e:
        current_app.logger.error(f"Error retrieving data: {str(e)}")
        return 'Error fetching data'

    # Post the retrieved data to the Fission router for enqueueing
    try:
        response = requests.post(url='http://router.fission/enqueue/traffic_accidents',
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(data)
                    )
        current_app.logger.info(f"Post response status: {response.status_code}, body: {response.text}")
    except Exception as e:
        current_app.logger.error(f"Error posting data: {str(e)}")
        return 'Error posting data'
    return 'OK'

