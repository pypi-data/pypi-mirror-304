import unittest
from pd_fred.data_fetcher import DataFetcher

class TestDataFetcher(unittest.TestCase):
    def test_fetch_data(self):
        # Example test, replace with real FRED API key and series ID for testing
        api_key = 'your_fred_api_key'
        fetcher = DataFetcher(api_key)
        data = fetcher.get_data('DGS10')
        self.assertFalse(data.empty)

if __name__ == '__main__':
    unittest.main()
