import requests
import json
import time
# URL to fetch the weather data
source_url = "http://www.bom.gov.au/fwo/" #  add IDV60901/IDV60901.95936.json
link_to_check_format = "http://www.bom.gov.au/climate/cdo/about/site-num.shtml"

vic_id = "IDV60801"
all_melbourne_id = "IDV60900"

# sydney station 046000 - 075999
# sydney station 146000 - 175999
# victoria station 076000 - 090999
# victoria station 176000 - 190999
sydney_station = list(range(46000, 75999)) + list(range(146000, 175999))
victoria_station = list(range(94839, 190999)) #list(range(76000, 90999)) +
def fetch_weather_data(url):
    """Fetches weather data from the given URL and saves it locally."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data: HTTP Status {}".format(response.status_code))


def save_data_locally(data, filename):
    """Saves the fetched data to a local file."""
    with open(filename, 'a') as file:
        json.dump(data, file, indent=4)
    print(f"Data successfully saved to {filename}")


def main():
    station = ""
    # Fetch the weather data
    for area in victoria_station:
        try:
            station = str(area)
            t_url = source_url + vic_id + "/" + vic_id + "." + station + ".json"
            print(t_url)
            weather_data = fetch_weather_data(t_url)

            # Save the data locally
            save_data_locally(weather_data, "Data/Weather_Data")
            time.sleep(2)

        except Exception as e:
            time.sleep(2)
            print(str(e))


if __name__ == "__main__":
    main()