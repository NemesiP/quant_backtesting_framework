import numpy as np

class PerformanceMetrics:
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
        excess_returns = returns - risk_free_rate
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
        return sharpe_ratio

    @staticmethod
    def calculate_max_drawdown(portfolio_values):
        """
        Calculate the maximum drawdown of the portfolio.

        :param portfolio_values: A list or array of portfolio values over time.
        :return: The maximum drawdown as a positive number.
        """
        # Convert the portfolio values to a numpy array for efficient calculations
        portfolio_values = np.array(portfolio_values)

        # Calculate the cumulative maximum value at each point in time
        cumulative_max = np.maximum.accumulate(portfolio_values)

        # Calculate drawdowns at each point as the percentage drop from the peak
        drawdowns = (cumulative_max - portfolio_values) / cumulative_max

        # Maximum drawdown is the largest of these values
        max_drawdown = np.max(drawdowns)

        return max_drawdown

"""
# Example Usage
# Assuming 'portfolio_returns' is a list of daily portfolio returns
sharpe_ratio = PerformanceMetrics.calculate_sharpe_ratio(portfolio_returns)
max_drawdown = PerformanceMetrics.calculate_max_drawdown(portfolio_values)
"""