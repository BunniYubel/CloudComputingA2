from elasticsearch8 import Elasticsearch
from datetime import datetime
from flask import current_app, request
import requests
import json

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
    # Connect to the local elastic server
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic','elastic') #TODO replace with yaml reference
    )
    response = requests.get('http://router.fission/fission-function/wharvester').json()
    weather_data = response["observations"]["data"]
    # print("beofre return")
    # return str(weather_data)
    print("before insertion")
    for data in weather_data:
        print("inserted one")
        res = client.index(
        index='weather_data',
        id = data['aifstime_utc']+data['history_product'],
        document=data
        )
    return f"finished. Inserted {len(weather_data)} entries"
    
