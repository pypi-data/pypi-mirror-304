# pd_fred

A Python package for calculating the Probability of Default (PD) using FRED data.

## Installation
```bash
pip install pd_fred
```

## Usage
```python
from pd_fred import DataFetcher, PDefaultCalculator

# Fetch data
fetcher = DataFetcher(api_key='your_fred_api_key')
data = fetcher.get_data('DGS10')

# Calculate PD using the Merton model
pd_value = PDefaultCalculator.calculate_merton_model(
    asset_value=100, debt_value=80, asset_volatility=0.2, risk_free_rate=0.01, time_horizon=1
)
```
