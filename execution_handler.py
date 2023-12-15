class ExecutionHandler:
    def __init__(self, slippage_model, transaction_cost_model):
        self.slippage_model = slippage_model
        self.transaction_cost_model = transaction_cost_model

    def execute_order(self, order):
        """
        Simulates the execution of an order.
        """
        # Apply slippage model
        executed_price = self.apply_slippage(order)

        # Calculate transaction costs
        transaction_cost = self.calculate_transaction_cost(order)

        # Log the order execution details
        self.log_order_execution(order, executed_price, transaction_cost)
        return executed_price, transaction_cost

    def apply_slippage(self, order):
        """
        Applies the slippage model to the order.
        """
        # Implement slippage model logic
        return self.slippage_model.apply_slippage(order['price'])

    def calculate_transaction_cost(self, order):
        """
        Calculates transaction costs for the order.
        """
        # Implement transaction cost model logic
        return self.transaction_cost_model.calculate_cost(order['volume'])

    def log_order_execution(self, order, executed_price, transaction_cost):
        # Log details of the executed order
        pass

class BasicSlippageModel:
    def __init__(self, slippage_percent=0.05):
        self.slippage_percent = slippage_percent

    def apply_slippage(self, order_price):
        return order_price * (1 + self.slippage_percent / 100)

class BasicTransactionCostModel:
    def __init__(self, fixed_fee=1.0):
        self.fixed_fee = fixed_fee

    def calculate_cost(self, order_volume):
        return self.fixed_fee

"""
# Example Usage
slippage_model = ...  # Define slippage model
transaction_cost_model = ...  # Define transaction cost model
execution_handler = ExecutionHandler(slippage_model, transaction_cost_model)
executed_price, transaction_cost = execution_handler.execute_order(order)
"""