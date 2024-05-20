import json, logging
from elasticsearch8 import Elasticsearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
    #open all states income json file
    with open('filtered_NSW_VIC_income.json', 'r') as file:
        individual_income = json.load(file)
    
    logger.info(f'Observations to add: {individual_income}')

    for obs in individual_income:
        res = client.index(
            index='individual_income',
            id=obs["lga_code"],
            body=obs
        )
        logger.info(f'Indexed observation {obs["lga_code"]}')

    return 'ok'

if __name__ == "__main__":
    main()
