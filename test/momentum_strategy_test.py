import unittest
import pandas as pd
import sys
 
# setting path
sys.path.append('../quant_backtesting_framework')
from quant_backtesting_framework.strategy import MomentumStrategy
from quant_backtesting_framework.data_handler import DataHandler

class TestMomentumStrategy(unittest.TestCase):
    def setUp(self):
        handler = DataHandler()
        self.data = handler.fetch_data(ticker="AAPL", start_date="2022-12-01", end_date="2023-12-01", add_all_technical_indicator=False)
        self.strategy = MomentumStrategy(self.data, lookback_period=60, long_momentum=2, short_momentum=-2)

    def test_generate_signals(self):
        signals = self.strategy.generate_signals()
        self.assertIsInstance(signals, list)
        if signals:
            self.assertIn('action', signals[0])
            self.assertIn('open_date', signals[0])
            self.assertIn('close_date', signals[0])

    def test_validate_inputs(self):
        with self.assertRaises(ValueError):
            self.strategy.validate_inputs(-1, 2, -2)
        with self.assertRaises(ValueError):
            self.strategy.validate_inputs(60, 'two', -2)
        with self.assertRaises(ValueError):
            self.strategy.validate_inputs(60, 2, 'minus two')

if __name__ == '__main__':
    unittest.main()