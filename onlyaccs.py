import aiohttp
import asyncio
import json
import logging
from retrying import retry
from typing import Optional

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
        'l': 'en',
        'p': page,
    }

    async with session.get(base_url, params=params, cookies=cookies, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            with open('aggregated_data.json', 'a') as f:
                json.dump(data, f, indent=4)
            logging.info(f'Data for page {page} saved successfully.')
            return data
        else:
            logging.error(f'Failed to fetch data for page {page}. Status code: {response.status}')
            return None

async def fetch_all_data(total_pages: int):
    """Fetch data for all pages."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_save_data(session, page) for page in range(500, total_pages + 1)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(fetch_all_data(1000))