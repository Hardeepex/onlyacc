import glob
import json

file_names = glob.glob('data_page_*.json')
combined_data = []

for file_name in file_names:
    with open(file_name, 'r') as f:
        data = json.load(f)
        combined_data.append(data)

with open('combined_data.json', 'w') as f:
    json.dump(combined_data, f)

print("Data has been successfully combined and written to combined_data.json")
