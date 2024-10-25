import unittest
from pd_fred.pd_calculator import PDefaultCalculator

class TestPDefaultCalculator(unittest.TestCase):
    def test_calculate_merton_model(self):
        result = PDefaultCalculator.calculate_merton_model(
            asset_value=100, debt_value=80, asset_volatility=0.2, risk_free_rate=0.01, time_horizon=1
        )
        self.assertGreater(result, 0)

if __name__ == '__main__':
    unittest.main()
