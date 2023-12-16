class ExecutionHandler:
    """
    The ExecutionHandler simulates the process of sending orders to a brokerage.
    It includes aspects like slippage and transaction costs.

    Attributes:
    slippage_model (BasicSlippageModel): The slippage model.
    transaction_cost_model (BasicTransactionCostModel): The transaction cost model.
    spread_percent (float): The spread percentage.
    """

    def calculate_transaction_cost(self, order, is_long):
        """
        Calculate the transaction cost for the given order.

        Args:
        order (dict): The order to calculate the transaction cost for. It should have 'quantity' and 'price' keys.
        is_long (bool): Whether the order is a long order.

        Returns:
        float: The transaction cost.
        """
        return self.transaction_cost_model.calculate_cost(order['quantity'], order['price'], is_long)

    def log_order_execution(self, order, executed_price, transaction_cost):
        """
        Log the details of the executed order.

        Args:
        order (dict): The executed order.
        executed_price (float): The price at which the order was executed.
        transaction_cost (float): The transaction cost.
        """
        pass

    def create_bid_ask(self, close):
        """
        Create the bid and ask prices based on the close price.

        Args:
        close (float): The close price.

        Returns:
        tuple: The bid and ask prices.
        """
        bid_price = close + close * (1 - self.spread_percent)
        ask_price = close - close * (1 + self.spread_percent)
        return bid_price, ask_price

class BasicSlippageModel:
    """
    The BasicSlippageModel applies slippage to the order price.

    Attributes:
    slippage_percent (float): The slippage percentage.
    """

    def apply_slippage(self, order_price, is_long):
        """
        Apply slippage to the order price.

        Args:
        order_price (float): The order price.
        is_long (bool): Whether the order is a long order.

        Returns:
        float: The order price with slippage.
        """
        if is_long:
            return order_price * (1 + self.slippage_percent / 100)
        else:
            return order_price * (1 - self.slippage_percent / 100)

class BasicTransactionCostModel:
    """
    The BasicTransactionCostModel calculates the transaction cost for an order.

    Attributes:
    transaction_cost_percent (float): The transaction cost percentage.
    """

    def calculate_cost(self, order_quantity, order_price, is_long):
        """
        Calculate the transaction cost for the given order quantity and price.

        Args:
        order_quantity (int): The order quantity.
        order_price (float): The order price.
        is_long (bool): Whether the order is a long order.

        Returns:
        float: The transaction cost.
        """
        if is_long:
            return order_quantity * order_price * (self.transaction_cost_percent / 100)
        else:
            return order_quantity * order_price * (self.transaction_cost_percent / 100) * -1