import logging, json, requests, socket
import time
from flask import current_app
import os

def save_data_locally(data, filename):
    """Saves the fetched data to a local file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def post_data_server(data):
    try:
        response = requests.post(url='http://router.fission/enqueue/weather',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        current_app.logger.info(f"Post response status: {response.status_code}, body: {response.text}")
        return json.dumps({'status': response.status_code, 'body': response.text})
    except Exception as e:
        current_app.logger.error(f"Error posting data: {str(e)}")
        return json.dumps({'error': str(e)})

def fetch_weather_data(url):
    """Fetches weather data from the given URL and saves it locally."""
    current_app.logger.info(f"Fetching weather data from {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    current_app.logger.info(f"Request Headers: {response.request.headers}")
    current_app.logger.info(f"Response Status Code: {response.status_code}")
    current_app.logger.info(f"Response Headers: {response.headers}")
    current_app.logger.info(f"Response Body: {response.text}")
    time.sleep(0.1)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data: HTTP Status {}".format(response.status_code))

def generate_id(obs):
    return f'{obs["wmo"]}-{obs["aifstime_utc"]}'

def main():
    directory = "Data"
    count = 0
    if not os.path.exists(directory):
        os.makedirs(directory)
    source_url = "http://www.bom.gov.au/fwo/"  # add IDV60901/IDV60901.95936.json
    link_to_check_format = "http://www.bom.gov.au/climate/cdo/about/site-num.shtml"
    check_minuets = 10
    vic_id = "IDV60801"
    syd_id = "IDN60801"
    all_melbourne_id = "IDV60900"
    sydney_station = ['95916', '94741', '94716', '94995', '94700', '99132', '95541', '99759',
                      '94757', '94686', '95756', '94901', '95869', '94794', '99763', '95740', '94782',
                      '95717', '99108', '94937', '94599', '99997', '95721', '94921', '99755', '99145',
                      '94798', '94761', '95520', '94736', '99738', '99105', '94760', '99152', '95937',
                      '94776', '94799', '94721', '99754', '94598', '99129', '99742', '95761', '94691',
                      '99109', '95716', '94941', '94783', '99762', '95757', '95995', '99758', '94701',
                      '99133', '94582', '95686', '95940', '94740', '94890', '95766', '94589', '95727',
                      '94927', '99753', '94862', '95770', '99790', '94767', '99786', '94730', '95571',
                      '95697', '94710', '95681', '99071', '99134', '94751', '95707', '99118', '94792',
                      '95746', '99765', '95896', '94696', '95710', '94785', '95747', '99764', '94910',
                      '94793', '94843', '95706', '94750', '99135', '94711', '94592', '94746', '95784',
                      '95570', '99787', '95527', '94766', '94789', '95931', '99791', '94727', '94926',
                      '99752', '95771', '94588', '95726', '95767', '99946', '94732', '95748', '94765',
                      '94909', '99792', '94773', '95709', '95772', '94925', '95908', '95725', '94708',
                      '95699', '94933', '94749', '94694', '94944', '94769', '95744', '94790', '95752',
                      '94728', '95705', '95512', '94929', '99136', '95729', '94587', '99823', '94712',
                      '95695', '95768', '94744', '99064', '95682', '95728', '99072', '94928', '94752',
                      '95704', '94729', '95753', '95929', '99789', '95745', '95895', '94768', '94748',
                      '94877', '95765', '95909', '95773', '94725', '95708', '95925', '94772', '99793',
                      '94764', '95749', '94733', '94699', '94692', '94738', '95715', '94780', '94915',
                      '99761', '94796', '95754', '94755', '95778', '94702', '94714', '99825', '99063',
                      '94743', '94939', '95719', '99106', '94919', '94763', '95758', '94775', '99110',
                      '99757', '95774', '94923', '94759', '95723', '95735', '95762', '99468', '94934',
                      '95734', '95722', '94758', '99756', '94689', '94723', '99111', '99146', '94774',
                      '95935', '94918', '99107', '94735', '95718', '94938', '95692', '94596', '94715',
                      '99824', '94650', '95684', '94996', '99998', '94703', '95779', '94754', '94797',
                      '99760', '94781', '95485', '94943', '94693']
    victoria_station = ['94891', '95853', '94829', '95941', '95845', '94844', '94852', '95890',
                        '94872', '94833', '94864', '95832', '99811', '99796', '95873', '95936', '99806',
                        '95825', '95872', '94849', '95864', '95833', '99810', '94920', '94865', '94824',
                        '95829', '94853', '94900', '95901', '94886', '94828', '94874', '94835', '94862', '99817',
                        '99051', '94858', '95822', '99047', '94878', '95855', '99821', '94839', '94881', '95843',
                        '95838', '94842', '94854', '94911', '95896', '94855', '95881', '94843', '94906', '95839',
                        '95907', '94880', '94838', '99066', '99820', '94879', '94859', '95874', '99816', '95835',
                        '99050', '94863', '94834', '94930', '94875', '99053', '95836', '99815', '94860', '94837',
                        '94876', '94933', '94899', '99049', '94913', '94856', '94905', '94840', '99819', '95904',
                        '94883', '94895', '94894', '95913', '99822', '94882', '95840', '99818', '94912', '94857',
                        '99048', '94932', '94898', '94836', '94861', '99052', '95837', '99814', '94908', '94949',
                        '99809', '94903', '94846', '94893', '95826', '99901', '95867', '99813', '94866', '94889',
                        '94831', '94827', '94870', '94935', '95918', '94871', '94826', '94830', '94888', '99054',
                        '99812', '95831', '99900', '95866', '99795', '95827', '94892', '94884', '94847', '94914',
                        '94693']

    for id in (vic_id, syd_id):
        if id == vic_id:
            loc = "VIC"
            station = victoria_station
        else:
            loc = "NSW"
            station = sydney_station
        for area in station:
            station = str(area)
            t_url = source_url + id + "/" + id + "." + station + ".json"
            data = fetch_weather_data(t_url)
            for obs in data['observations']['data']:
                obs_id = generate_id(obs)
                # Save or post data with the generated id
                # Example: save_data_locally(obs, f"{obs_id}.json")
                # Example: post_data_server(obs)
                current_app.logger.info(f'Generated ID: {obs_id}')
                # For debugging
                return obs

if __name__ == "__main__":
    main()
