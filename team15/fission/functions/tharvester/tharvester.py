import csv
import pandas as pd
import logging, json, requests, socket
import time
from flask import current_app
import os

api_url = "https://data.gov.au/data/api/3/action/datastore_search?resource_id=d54f7465-74b8-4fff-8653-37e724d0ebbb&q=2023&limit=100000"
#output_file = "2023_Traffic_Accidents.json"  # Output JSON file path

#input_json = output_file
#output_json = "2023_TA_Records.json"
#output_csv = "2023_TA_Records.csv"

# Grabbing information from API URL and turning it into a JSON
def URL_to_JSON(url):
    try:
        response = requests.get(url)
        data = response.json()
        logging.info("Data fetched successfully from URL.")
        return data
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    # Create and Write to a JSON file
    #with open(filename, 'w') as json_file:
    #    json.dump(data, json_file, indent=4)

def get_Records(data):
    """"
def get_Records(input_file, output_file):
    with open(input_file, 'r') as json_file:
            data = json.load(json_file)
            # Upon inspecting the JSON file, the data we're interested in is under 'records'
            records = data["result"]["records"]

            records_data = {"records": records}
            with open(output_file, 'w') as output_json_file:
                json.dump(records_data, output_json_file, indent=4)
    """
    try:
        records = data["result"]["records"]
        logging.info("Records extracted successfully.")
        return records
    except KeyError as e:
        logging.error(f"Key error: {e}")
    except TypeError as e:
        logging.error(f"Type error: {e}")

def convert_json_csv(records):
    # Define the features you want to extract from each record
    features = [
        "_id", "Crash ID", "State", "Month", "Year", "Dayweek", "Time", 
        "Crash Type", "Number Fatalities", "Bus \nInvolvement", 
        "Heavy Rigid Truck Involvement", "Articulated Truck Involvement", 
        "Speed Limit", "National Remoteness Areas", "SA4 Name 2021", 
        "National LGA Name 2021", "National Road Type", "Christmas Period", 
        "Easter Period", "Day of week", "Time of Day", "rank"
    ]
    
    # Log each record with the specified features
    for record in records:
        filtered_record = {key: record.get(key, '') for key in features}
        logging.info(filtered_record)

def main():
    # Fetch data from API and log it
    data = URL_to_JSON(api_url)
    # Extract records and log them
    records = get_Records(data)
    # Convert records to CSV format and log them
    convert_json_csv(records)

if __name__ == "__main__":
    main()

"""
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

#URL_to_JSON(api_url, output_file)
#get_Records(input_json, output_json)
#convert_json_csv(output_json, output_csv)
"""
