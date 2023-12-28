import requests
import json
import time

# Base URL, cookies, and headers from your successful code
base_url = 'https://onlyaccounts.io/api/filter'
cookies = {
    '_ga_FDKG0GFFWX': 'GS1.1.1703660630.1.0.1703660630.60.0.0',
    '_ga': 'GA1.1.461595529.1703660630',
}
headers = {
    'authority': 'onlyaccounts.io',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    'referer': 'https://onlyaccounts.io/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
}
def fetch_and_save_data(page):
    params = {
        'q': 'best-onlyfans',
        'l': 'en',
        'p': page,
    }

    response = requests.get(base_url, params=params, cookies=cookies, headers=headers)
    if response.ok:
        data = response.json()
        with open(f'data{page}.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f'Data for page {page} saved successfully.')
        return data
    else:
        print(f'Failed to fetch data for page {page}. Status code: {response.status_code}')
        if response.text:
            print("Response text:", response.text)  # Log detailed error message if available
        return None

def fetch_all_data(total_pages):
    for page in range(500, total_pages + 1):
        print(f"Fetching data for page {page}...")
        fetch_and_save_data(page)
        time.sleep(1)  # Sleep to respect rate limits

# Example usage:
fetch_all_data(1000)