import json

file_path = "/Users/YangWei-Chiao/CloudComputingA2/Data/Income_Distribution/abs_personal_income_total_income_distribution_lga_2015_16-9160214636052902521.json"

with open(file_path) as file:
    data = json.load(file)
features = data["features"]
preprocess_info = [feature["properties"] for feature in features]

#lga code for NSW starts with 1, VIC starts with 2
filtered_NSW_VIC_data = [feature for feature in features if feature["properties"]["lga_code"].startswith(("1", "2"))]
preprocess_filtered_NSW_VIC_data = [feature["properties"] for feature in filtered_NSW_VIC_data]
# print(filtered_NSW_VIC_data)

with open('all_states_income.json', 'w') as file:
    for item in preprocess_info:
        file.write(json.dumps(item) + '\n')

with open('filtered_NSW_VIC_income.json', 'w') as file:
    for item in preprocess_filtered_NSW_VIC_data:
        file.write(json.dumps(item) + '\n')
