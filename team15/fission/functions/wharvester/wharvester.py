import logging, json, requests, socket
import stat
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
        # current_app.logger.info(f"Post response status: {response.status_code}, body: {response.text}")
        return json.dumps({'status': response.status_code, 'body': response.text})
    except Exception as e:
        # current_app.logger.error(f"Error posting data: {str(e)}")
        return json.dumps({'error': str(e)})

def fetch_weather_data(url):
    """Fetches weather data from the given URL and saves it locally."""
    # current_app.logger.info(f"Fetching weather data from {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data: HTTP Status {}".format(response.status_code))

def generate_id(obs):
    return f'{obs["wmo"]}-{obs["aifstime_utc"]}'

def main():
    current_app.logger.info("start!")
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
    station_dictionary = {
                "IDD60801": ['94000', '94002', '94003',
                      '94100', 94102, 94105, 94106, 94108, 94109, 94110, 94112, 94114, 94116, 94117, 94119, 94120, 94121, 94122, 94125, 94127, 94128, 94130, 94131, 94132, 94134, 94135, 94137, 94139, 94140, 94141, 94143, 94147, 94150, 94152, 94153, 94161, 94162, 94212, 94216, 94217, 94220, 94221, 94222, 94225, 94229, 94231, 94232, 94234, 94236, 94237, 94238, 94239, 94242, 94248, 94255, 94258, 94321, 94322, 94323, 94324, 94325, 94326, 94327, 94328, 94457, 94461, 94462, 94463, 94466, 94474, 95101, 95111, 95121, 95122, 95142, 95146, 95214, 95215, 95322, 95323],
        "IDQ60801": [94004, 94170, 94171, 94174,
                          94181, 94182, 94183, 94186, 94188, 94254, 94255, 94257, 94260, 94261, 94266, 94268, 94270, 94271, 94272, 94273, 94274, 94275, 94276, 94280, 94284, 94285, 94287, 94288, 94289, 94290, 94291, 94292, 94293, 94294, 94295, 94297, 94298, 94299, 94332, 94333, 94334, 94335, 94336, 94337, 94338, 94341, 94342, 94343, 94344, 94345, 94346, 94347, 94348, 94349, 94350, 94352, 94355, 94356, 94359, 94360, 94363, 94365, 94367, 94368, 94370, 94371, 94372, 94373, 94374, 94376, 94377, 94378, 94379, 94380, 94381, 94383, 94384, 94386, 94387, 94388, 94390, 94393, 94394, 94395, 94396, 94397, 94398, 94399, 94418, 94419, 94420, 94489, 94500, 94510, 94511, 94513, 94514, 94515, 94517, 94521, 94525, 94542, 94547, 94548, 94549, 94550, 94552, 94553, 94555, 94561, 94562, 94564, 94566, 94567, 94568, 94569, 94570, 94575, 94576, 94577, 94578, 94580, 94581, 94584, 94590, 94591, 94592, 94593, 94594, 95283, 95286, 95288, 95291, 95292, 95293, 95295, 95296, 95298, 95351, 95362, 95367, 95369, 95370, 95482, 95487, 95492, 95529, 95533, 95543, 95551, 95565, 95566, 95572, 95575, 95581, 95591],
        "IDS60801": [94474, 94476, 94648, 94651, 94653, 94654, 94655, 94656, 94657, 94659, 94660, 94661, 94662, 94663, 94665, 94666, 94668, 94672, 94673, 94674, 94676, 94677, 94678, 94679, 94680, 94681, 94682, 94683, 94684, 94685, 94690, 94804, 94806, 94807, 94808, 94809, 94811, 94813, 94814, 94816, 94817, 94820, 94821, 94822, 95458, 95480, 95481, 95649, 95652, 95654, 95658, 95659, 95660, 95661, 95662, 95663, 95664, 95666, 95667, 95668, 95669, 95670, 95671, 95674, 95675, 95676, 95677, 95678, 95679,
                     95683, 95687, 95805, 95806, 95807, 95811, 95812, 95813, 95814, 95815, 95816, 95818, 95823],
        "IDT60801": [94619, 94850, 94949, 94950, 94951, 94953, 94955, 94956, 94957, 94958, 94959, 94960, 94961, 94962, 94963, 94964, 94966, 94967, 94969, 94970, 94971, 94972, 94974, 94975, 94976, 94977, 94979, 94980, 94981, 94983, 94985, 94987, 94988, 94998, 95952, 95953, 95954, 95956, 95957, 95958, 95959, 95960, 95961, 95962, 95963, 95964, 95966, 95967, 95970,
                     95972, 95973, 95975, 95977, 95979, 95981, 95984, 95985, 95986, 95987, 95988, 95989],
        "IDW60801": [94100, 94102, 94103, 94200, 94201, 94202, 94203, 94204, 94206, 94207, 94210, 94211, 94212, 94213, 94215, 94216, 94217, 94300, 94302, 94303, 94306, 94307, 94308, 94310, 94311, 94312, 94314, 94316, 94317, 94318, 94319, 94320, 94330, 94401, 94402, 94403, 94404, 94405, 94410, 94411, 94414, 94415, 94417, 94422, 94429, 94430, 94439, 94440, 94444, 94448, 94449, 94450, 94451, 94457, 94461, 94600, 94601, 94602, 94603, 94604, 94605, 94607, 94608, 94609, 94610, 94612, 94614, 94615, 94617, 94620, 94621, 94622, 94623, 94625, 94626, 94627, 94628, 94630, 94631, 94632, 94633, 94634, 94636, 94637, 94638, 94640, 94641, 94642, 94643, 94644, 94645, 94647, 94795, 94801, 94802, 95101, 95202, 95204, 95205, 95208, 95214, 95215, 95303, 95304, 95305, 95307, 95316, 95317, 95402, 95439, 95448, 95600, 95601, 95602, 95603, 95604, 95605, 95606, 95607, 95608, 95609, 95610, 95611, 95612, 95613, 95614, 95615, 95616, 95617, 95618, 95620, 95621, 95622, 95623, 95624, 95625, 95626, 95627, 95628, 95629, 95630, 95631, 95632,
                     95634, 95635, 95636, 95637, 95638, 95639, 95640, 95641, 95642, 95644, 95646, 95647, 95648],
        "IDV60801": ['94891', '95853', '94829', '95941', '95845', '94844', '94852', '95890',
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
                        '94693'],
        "IDN60801": ['95916', '94741', '94716', '94995', '94700', '99132', '95541', '99759',
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

    }
    total_observations = 0
    # go through each state and get request data of each station
    for area_id in station_dictionary.keys():
        current_app.logger.info("inside!")
        for area in station_dictionary[area_id]:
            station = str(area) 
            t_url = source_url + area_id + "/" + area_id + "." + station + ".json" # build url
            data = fetch_weather_data(t_url)
            station_observations = data['observations']['data'] # get just data for station
            post_data_server(station_observations) # enqueue data to kafka
            total_observations += len(station_observations)
            current_app.logger.info(f"Got {len(station_observations)} observations from {area}. Total: {total_observations}!1")
if __name__ == "__main__":
    main()
