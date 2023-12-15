class RiskManagement:
    def __init__(self, max_drawdown, max_position_size):
        self.max_drawdown = max_drawdown
        self.max_position_size = max_position_size

    def assess_trade_risk(self, portfolio, proposed_trade):
        """
        Assess if a proposed trade complies with the risk parameters.
        """
        # Implement logic to evaluate trade risk here
        # For example, check if the trade exceeds the maximum position size
        #return is_within_risk_limits
        raise NotImplementedError

    def evaluate_portfolio_risk(self, portfolio):
        """
        Evaluates the overall risk of the portfolio.
        """
        # Implement logic to evaluate portfolio risk
        # For example, calculate portfolio drawdown
        #return is_within_risk_limits
        raise NotImplementedError

"""
# Example Usage
risk_manager = RiskManagement(max_drawdown=0.20, max_position_size=0.10)
if risk_manager.assess_trade_risk(portfolio, proposed_trade):
    # Execute trade
else:
    # Reject trade
"""
