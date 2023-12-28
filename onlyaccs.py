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
@retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
async def handle_response(session, response, page):
    """Handle response from API."""
    if response.status == 200:
        # handle success
        data = await response.json()
        with open('aggregated_data.json', 'a') as f:
            json.dump(data, f, indent=4)
        logging.info(f'Data for page {page} saved successfully.')
        return data
    elif response.status == 422:
        # handle unprocessable entity
        logging.error(f'Unprocessable entity, check parameters for page {page}.')
        return None
    elif response.status >= 500:
        # handle server errors
        logging.error(f'Server error while fetching data for page {page}. Retry later.')
        return None
    else:
        # handle other HTTP errors
        logging.error(f'HTTP error {response.status} for page {page}.')
        return None

@retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
async def fetch_and_save_data(page, session):
    """Fetch and save data for a given page."""
    # Validate parameters to avoid HTTP 422 errors
params = {
    'q': 'best-onlyfans',
    'l': 'en-US',
    'p': page
}
        'q': 'best-onlyfans',
        'l': 'en',
        'p': page
    }
    async with session.get(base_url, params=params, cookies=cookies, headers=headers) as response:
        return await handle_response(session, response, page)
    params = {
        'q': 'best-onlyfans',
        'l': 'en',
        'p': page,
        'l': 'en',
        'p': page,
    }

    async with session.get(base_url, params=params, cookies=cookies, headers=headers) as response:
        if response.status == 200:
            # handle success
            data = await response.json()
        elif response.status == 400:
            # handle bad request
            logging.error(f'Bad request error for page {page}.')
            return None
        elif response.status == 401:
            # handle unauthorized
            logging.error(f'Unauthorized access for page {page}.')
            return None
        elif response.status == 403:
            # handle forbidden
            logging.error(f'Forbidden access, rate limiting for page {page}.')
            return None
        elif response.status == 404:
            # handle not found
            logging.error(f'Page {page} not found.')
            return None
        elif response.status == 422:
            # handle unprocessable entity
            logging.error(f'Unprocessable entity, check parameters for page {page}.')
            return None
        elif response.status == 429:
            # handle too many requests, rate limiting
            logging.warning(f'Rate limited. Cooling down before retrying page {page}.')
            await asyncio.sleep(60)  # wait 60 seconds before retrying
            return await fetch_and_save_data(page, session)
        elif response.status == 500:
            # handle server errors
            logging.error(f'Server error while fetching data for page {page}.')
            return None
        else:
            # handle other errors
            logging.error(f'Failed to fetch data for page {page}. Status code: {response.status}')
            return None
            data = await response.json()
            with open('aggregated_data.json', 'a') as f:
                json.dump(data, f, indent=4)
            logging.info(f'Data for page {page} saved successfully.')
            return data
        else:
            logging.error(f'Failed to fetch data for page {page}. Status code: {response.status}')
            return None

async def fetch_paginated_data(start_page: int, total_pages: int, session: aiohttp.ClientSession):
    """Fetches data page by page and saves it.

    Args:
        start_page (int): The starting page number for the data fetching.
        total_pages (int): The total number of pages to fetch.
        session (aiohttp.ClientSession): The session used for HTTP requests.
    """
    """Fetch paginated data in a range of pages."""
    for page in range(start_page, total_pages + 1):
        await fetch_and_save_data(page, session)

async def fetch_all_data(total_pages: int):
    """Main function to fetch data from all pages.

    It starts from a given page (in this case, 500) and continues until the reported total
    number of pages is reached, updating the total if necessary.

    Args:
        total_pages (int): The total number of pages to fetch (initial estimate).
    """
    """Fetch data for all pages."""
    async with aiohttp.ClientSession() as session:
        # Start from page 500 and dynamically determine the actual total pages
        start_page = 500
        response = await session.get(base_url, params={'p': start_page}, cookies=cookies, headers=headers)
        if response.status == 200:
            data = await response.json()
            # Assume the 'total' key in the response contains the actual total page count
            actual_total_pages = data.get('total', total_pages)
            await fetch_paginated_data(start_page, actual_total_pages, session)
        elif response.status == 429:
            # Handle rate limiting
            logging.warning('Rate limited. Cooling down before retry.
            await asyncio.sleep(60)  # Wait 60 seconds before retrying
            await fetch_paginated_data(start_page, total_pages, session)
    """Fetch data for all pages."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_save_data(page) for page in range(500, total_pages + 1)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(fetch_all_data(1000))