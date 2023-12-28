import unittest
import asyncio
from unittest.mock import patch

from onlyaccs import fetch_all_data, fetch_and_save_data


class TestOnlyAccs(unittest.IsolatedAsyncioTestCase):

    @patch('aiohttp.ClientSession.get', new_callable=unittest.mock.AsyncMock)
    async def test_fetch_and_save_data(self, mock_get):
        mock_get.return_value.status = 200
        mock_get.return_value.json.return_value = {"test": "data"}
        result = await fetch_and_save_data(1)
        self.assertEqual(result, {"test": "data"})

    @patch('aiohttp.ClientSession.get')
    async def test_fetch_all_data(self, mock_get):
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json.return_value = {"test": "data"}
        await fetch_all_data(1)
        mock_get.assert_called_once()

if __name__ == '__main__':
        asyncio.run(unittest.main())
