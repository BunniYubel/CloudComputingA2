import requests
import json
import time
import os
from datetime import datetime, timedelta
current_time = datetime.now()
format = '%I:%M%p'
c_YM = current_time.strftime('%y:%m')
c_date = current_time.strftime('%d')
c_time = current_time.strftime('%I:%M%p')
c_time = datetime.strptime(c_time, format)
# URL to fetch the weather data
source_url = "http://www.bom.gov.au/fwo/" #  add IDV60901/IDV60901.95936.json
link_to_check_format = "http://www.bom.gov.au/climate/cdo/about/site-num.shtml"
check_minuets = 120
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
victoria_station = list(range(94800, 99999)) #list(range(76000, 90999)) +
def fetch_weather_data(url):
    """Fetches weather data from the given URL and saves it locally."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    time.sleep(0.1)
    if response.status_code == 200:

        return response.json()
    else:
        raise Exception("Failed to fetch data: HTTP Status {}".format(response.status_code))


def save_data_locally(data, filename):
    """Saves the fetched data to a local file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def process_weather_data(item):
    """Process a single data entry and return a dictionary of specific attributes."""
    name_with_underscores = item['name'].replace(' ', '_')

    check_time = item['local_date_time'].split("/")[1]

    datetime1 = datetime.strptime(check_time, format)
    minutes_diff = (c_time - datetime1).total_seconds() / 60.0
    if item['local_date_time'].split("/")[0] == c_date and minutes_diff <= check_minuets:
        key = name_with_underscores
        values = {
            'date': c_YM + ":" + c_date + ":" + check_time,
            'weather': item['weather'],
            'rel_hum': item['rel_hum'],
            'air_temp': item['air_temp'],
            'cloud': item['cloud'],
            'rain_trace': item['rain_trace'],
            'wind_spd_kmh': item['wind_spd_kmh']
        }
    else:
        return "None", "None"
    return key, values

def main():
    station = ""
    # Ensure the directory exists
    directory = "Data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Fetch the weather data
    for area in victoria_station:
        try:
            station = str(area)
            t_url = source_url + vic_id + "/" + vic_id + "." + station + ".json"
            print(t_url)
            weather_data = fetch_weather_data(t_url)

            # Save the data locally
            save_data_locally(weather_data, f"Data/Weather_Data_{station}.json")
            time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching data for station {station}: {str(e)}")

if __name__ == "__main__":
    main()
