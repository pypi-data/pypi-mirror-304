from fredapi import Fred
import pandas as pd

class DataFetcher:
    def __init__(self, api_key):
        self.fred = Fred(api_key=api_key)

    def get_data(self, series_id, start_date=None, end_date=None):
        data = self.fred.get_series(series_id, start_date, end_date)
        return pd.DataFrame(data, columns=['Value']).reset_index().rename(columns={'index': 'Date'})
