import unittest
import pandas as pd
from data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DataHandler()

    def test_fetch_data(self):
        data = self.handler.fetch_data("AAPL", "2020-01-01", "2021-01-01")
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)

    def test_add_all_technical_indicator(self):
        data = pd.DataFrame(data={
            'open': [x for x in range(1, 61)],
            'high': [x for x in range(1, 61)],
            'low': [x for x in range(1, 61)],
            'close': [x for x in range(1, 61)],
            'volume': [10 for x in range(1, 61)]
        }, index=pd.date_range(start='2020-01-01', periods=60, freq='D'))
        data = self.handler.add_all_technical_indicator(data)
        self.assertTrue('volume_adi' in data.columns)

    def test_lower_column_names(self):
        data = pd.DataFrame({
            'Open': [x for x in range(1, 60)],
            'High': [x for x in range(1, 60)],
            'Low': [x for x in range(1, 60)],
            'Close': [x for x in range(1, 60)],
            'Volume': [10 for x in range(1, 60)]
        })
        data = self.handler.lower_column_names(data)
        self.assertTrue('open' in data.columns)

if __name__ == "__main__":
    unittest.main()