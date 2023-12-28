import requests
import json
import time

# Define the base URL and headers for the API request
base_url = 'https://onlysearch.co/api/search'
headers = {
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Referer': 'https://onlysearch.co/profiles?keyword=',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua-platform': '"Android"',
}

# Function to fetch data and save it to a JSON file.
def fetch_and_save_data(page):
    params = {
        'keyword': '',
        'location': '',
        'sortBy': '',
        'priceFrom': '0',
        'priceTo': '50',
        'page': page,
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.ok:
        data = response.json()
        with open(f'data_page_{page}.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f'Data for page {page} saved successfully.')
        return data
    else:
        print(f'Failed to fetch data for page {page}. Status code: {response.status_code}')
        return None

# Function to fetch all pages.
def fetch_all_data():
    page = 500
    all_data_collected = False
    while not all_data_collected:
        data = fetch_and_save_data(page)
        if data is None or not data.get('hasMore', True):  # Assuming 'hasMore' indicates more pages
            all_data_collected = True
        else:
            page += 1
            time.sleep(1)  # Sleep to respect rate limits

# Start the data fetching process.
fetch_all_data()
