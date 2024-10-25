import numpy as np
from scipy.stats import norm

class PDefaultCalculator:
    @staticmethod
    def calculate_merton_model(asset_value, debt_value, asset_volatility, risk_free_rate, time_horizon):
        d1 = (np.log(asset_value / debt_value) + (risk_free_rate + 0.5 * asset_volatility ** 2) * time_horizon) /
              (asset_volatility * np.sqrt(time_horizon))
        d2 = d1 - asset_volatility * np.sqrt(time_horizon)
        pd = 1 - norm.cdf(d2)
        return pd
