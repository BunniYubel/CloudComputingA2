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

    output_file = "2023_Traffic_Accidents.json"  # Output JSON file path
    input_json = output_file
    output_json = "2023_TA_Records.json"
    filtered_json = "Filtered_2023_TA_Records.json"
    clean_json = "Clean_2023_TA_Records.json"

    # Construct the API URL with the configured parameters
    api_url = f"{base_url}?resource_id={resource_id}&q={year}&limit={limit}"

    # Send a GET request to the API URL and retrieve the data as JSON
    URL_to_JSON(api_url, output_file)
    get_Records(input_json, output_json)
    filter_Records(output_json, filtered_json)
    clean_data(filtered_json, clean_json)

    current_app.logger.info("Getting information as JSON")
    data = json.load(filtered_json)
    # Post the retrieved data to the Fission router for enqueueing
    requests.post(url='http://router.fission/enqueue/traffic_accidents',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(data)
                  )
    return 'OK'

def URL_to_JSON(url, filename):
    read_link = requests.get(url)

    data = read_link.json()

    # Create and Write to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def get_Records(input_file, output_file):
    with open(input_file, 'r') as json_file:
            data = json.load(json_file)
            # Upon inspecting the JSON file, the data we're interested in is under 'records'
            records = data["result"]["records"]

            records_data = {"records": records}
            with open(output_file, 'w') as output_json_file:
                json.dump(records_data, output_json_file, indent=4)

def convert_json_csv(input_file, output_file):
     with open(input_file, 'r') as json_file:
            data = json.load(json_file)
            records = data["records"]
            # Below are all the data that is stored for each car accident
            features = [
                "_id", "Crash ID", "State", "Month", "Year", "Dayweek", "Time", 
                "Crash Type", "Number Fatalities", "Bus \nInvolvement", 
                "Heavy Rigid Truck Involvement", "Articulated Truck Involvement", 
                "Speed Limit", "National Remoteness Areas", "SA4 Name 2021", 
                "National LGA Name 2021", "National Road Type", "Christmas Period", 
                "Easter Period", "Day of week", "Time of Day", "rank"
            ]

            # Creating a new line in the csv for each car crash with the corresponding features listed above
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=features)
                writer.writeheader()
                for record in records:
                    # Filter record data based on fieldnames
                    filtered_record = {key: record.get(key, '') for key in features}
                    writer.writerow(filtered_record)

def filter_Records(input_file, output_file):
    filtered_records = []
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)
        for record in data['records']:
            filtered_record = {
                "State": record["State"],
                "Month": record["Month"],
                "Year": record["Year"],
                "Time": record["Time"],
                "Number Fatalities": record["Number Fatalities"],
                "Speed Limit": record["Speed Limit"]
            }
            filtered_records.append(filtered_record)
        filtered_data = {
         "records": filtered_records
        }
    
    with open(output_file, 'w') as file:
        json.dump(filtered_data, file, indent=4)

def clean_data(input_file, output_file):
    clean_records = []
    with open(input_file, 'r') as file:
        data = json.load(file)
        for record in data['records']:
            if (
                record.get('State') is not None and not record.get('State').isdigit() and
                record.get('Time') is not None and
                record.get('Number Fatalities') is not None and
                record.get('Speed Limit') is not None and record.get('Speed Limit').isdigit() and int(record.get('Speed Limit')) >= 0 and
                record.get('Month') is not None and
                record.get('Year') is not None
            ):
                clean_records.append(record)

    with open(output_file, 'w') as file:
         json.dump(clean_records, file, indent=4)  