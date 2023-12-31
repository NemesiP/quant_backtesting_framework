class Portfolio:
    def __init__(self, initial_cash):
        self.cash = initial_cash
        self.positions = {}
        self.transaction_log = []
        self.total_value = initial_cash
        self.total_value_history = [initial_cash]  # New attribute to store the portfolio value history

    def update_position(self, ticker, quantity, price, signal):
        if signal == 'BUY' and self.cash >= quantity * price:
            self.cash -= quantity * price
            self.positions[ticker] = self.positions.get(ticker, 0) + quantity
            self.transaction_log.append((ticker, quantity, price, 'BUY'))
        elif signal == 'SELL':
            if ticker in self.positions and self.positions.get(ticker, 0) >= quantity:
                self.cash += quantity * price
                self.positions[ticker] -= quantity
                if self.positions[ticker] == 0:
                    del self.positions[ticker]
                self.transaction_log.append((ticker, quantity, price, 'SELL'))
            else:
                print(f"Attempted to sell {quantity} of {ticker}, but you don't own any.")
        self.calculate_total_value(price)  # Calculate the total value after each trade

    def calculate_total_value(self, price):
        position_values = sum([quantity * price for ticker, quantity in self.positions.items()])
        self.total_value = self.cash + position_values
        self.total_value_history.append(self.total_value)  # Update the portfolio value history

    def handle_signals(self, signals, market_data):
        """
        Handles trading signals generated by a strategy.
        """
        for index, row in signals.iterrows():
            price = market_data.loc[index, 'close']
            quantity = self.cash // price  # Calculate the quantity based on the available cash and the current price
            if row['orders'] == 1.0:  # Buy signal
                self.update_position(index, quantity, price, 'BUY')
            elif row['orders'] == -1.0:  # Sell signal
                quantity = self.positions.get(index, 0)  # Sell all stocks of this type
                self.update_position(index, quantity, price, 'SELL')

        self.calculate_total_value(price)
        
if __name__ == '__main__':
    from data_handler import DataHandler
    from strategy import MomentumStrategy
    handler = DataHandler()
    data = handler.fetch_data("AAPL", "2020-01-01", "2021-01-01")  
    momentum_strategy = MomentumStrategy(data, lookback_period=30)
    signals = momentum_strategy.generate_signals()
    # Create a portfolio with an initial cash balance of 10000
    portfolio = Portfolio(10000)
    # Handle the trading signals
    portfolio.handle_signals(signals, data)
    # Recalculate the total portfolio value after handling all signals
    portfolio.calculate_total_value(data)
    # Print the final portfolio value
    print(portfolio.total_value)
    # Print the transaction log
    for transaction in portfolio.transaction_log:
        print(transaction)