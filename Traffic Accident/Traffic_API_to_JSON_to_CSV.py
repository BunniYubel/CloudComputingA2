import csv
import requests
import urllib.request
import json
import pandas as pd

api_url = "https://data.gov.au/data/api/3/action/datastore_search?resource_id=d54f7465-74b8-4fff-8653-37e724d0ebbb&q=2023&limit=100000"
output_file = "2023_Traffic_Accidents.json"  # Output JSON file path

input_json = output_file
output_json = "2023_TA_Records.json"
output_csv = "2023_TA_Records.csv"

# Grabbing information from API URL and turning it into a JSON
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

#URL_to_JSON(api_url, output_file)
#get_Records(input_json, output_json)
#convert_json_csv(output_json, output_csv)
