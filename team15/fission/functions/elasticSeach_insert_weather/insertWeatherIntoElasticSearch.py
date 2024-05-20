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
        basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD')) 
    )

    
    elasticsearch_index_name = "weather-data"
    index_config = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    }
    if not client.indices.exists(index=elasticsearch_index_name):
    # Create the index with the specified configuration
        client.indices.create(index=elasticsearch_index_name, body=index_config)
    

    response = requests.get('http://router.fission/fission-function/wharvester').json()
    weather_data = response["observations"]["data"]
    # print("beofre return")
    # return str(weather_data)
    print("before insertion")
    for data in weather_data:
        print("inserted one")
        res = client.index(
        index=elasticsearch_index_name,
        id = data['aifstime_utc']+data['history_product'],
        document=data
        )
    return f"finished. Inserted {len(weather_data)} entries"
    
