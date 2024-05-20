import logging, json
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic')
    )
    elasticsearch_index_name = "weather-data1"
    index_config = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    }
    if not client.indices.exists(index=elasticsearch_index_name):
    # Create the index with the specified configuration
        client.indices.create(index=elasticsearch_index_name, body=index_config)
    
    
    
    current_app.logger.info(f'Observations to add1:  {request.get_json(force=True)[0]}')

    for obs in request.get_json(force=True):
        res = client.index(
            index=elasticsearch_index_name,
            id=f'{obs["station_name"]}-{obs["timestamp"]}',
            document=obs
        )
        current_app.logger.info(f'Indexed observation: {obs["station_name"]}-{obs["timestamp"]}')

    return 'ok'
