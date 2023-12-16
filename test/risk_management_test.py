import unittest
import sys
 
# setting path
sys.path.append('../quant_backtesting_framework')
from quant_backtesting_framework.risk_management import RiskManagement
import numpy as np

class TestRiskManagement(unittest.TestCase):
    def setUp(self):
        self.portfolio_returns = np.array([0.01, -0.02, 0.03, -0.04, 0.05, -0.06, 0.07, -0.08, 0.09, -0.10])
        self.risk_manager = RiskManagement(self.portfolio_returns)

    def test_calculate_var(self):
        var = self.risk_manager.calculate_var(self.portfolio_returns, 0.95)
        expected_var = np.percentile(self.portfolio_returns, 5)
        self.assertEqual(var, expected_var)

    def test_calculate_cvar(self):
        cvar = self.risk_manager.calculate_cvar(self.portfolio_returns, 0.95)
        expected_cvar = self.portfolio_returns[self.portfolio_returns <= np.percentile(self.portfolio_returns, 5)].mean()
        self.assertEqual(cvar, expected_cvar)

    def test_calculate_max_drawdown(self):
        portfolio_values = np.array([100, 110, 105, 120, 115, 130, 125, 140, 135, 150])
        max_drawdown = self.risk_manager.calculate_max_drawdown(portfolio_values)
        running_max = np.maximum.accumulate(portfolio_values)
        drawdown = (running_max - portfolio_values) / running_max
        expected_max_drawdown = drawdown.max()
        self.assertEqual(max_drawdown, expected_max_drawdown)

if __name__ == '__main__':
    unittest.main()