import unittest
import sys
 
# setting path
sys.path.append('../quant_backtesting_framework')
from quant_backtesting_framework.execution_handler import ExecutionHandler

class TestExecutionHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ExecutionHandler()

    def test_create_bid_ask(self):
        bid_price, ask_price = self.handler.create_bid_ask(100)
        self.assertEqual(bid_price, 100.00099)
        self.assertEqual(ask_price, 99.99901)

    def test_apply_slippage(self):
        long_price = self.handler.apply_slippage({'price': 100}, True)
        short_price = self.handler.apply_slippage({'price': 100}, False)
        self.assertEqual(long_price, 100.05)
        self.assertEqual(short_price, 99.95)

    def test_calculate_transaction_cost(self):
        long_cost = self.handler.calculate_transaction_cost({'quantity': 10, 'price': 100}, True)
        short_cost = self.handler.calculate_transaction_cost({'quantity': 10, 'price': 100}, False)
        self.assertEqual(long_cost, 10)
        self.assertEqual(short_cost, -10)

if __name__ == '__main__':
    unittest.main()