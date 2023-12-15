from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import logging

class Strategy(ABC):
    """
    Abstract base class for trading strategies.
    """

    @abstractmethod
    def generate_strategy_column(self):
        """
        Generates a new column in the DataFrame containing the strategy logic.
        Must be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def generate_signals(self):
        """
        Generates trading signals based on strategy logic.
        Must be implemented by all subclasses.
        """
        pass

class MomentumStrategy:
    """
    A class used to represent a Momentum Strategy for trading.

    ...

    Attributes
    ----------
    data : pandas.DataFrame
        a pandas DataFrame containing the market data
    lookback_period : int
        the number of periods to look back for calculating momentum
    long_momentum : int or float
        the threshold for long momentum
    short_momentum : int or float
        the threshold for short momentum
    logger : logging.Logger
        a logger for logging events

    Methods
    -------
    validate_inputs(lookback_period, long_momentum, short_momentum):
        Validates the inputs for the strategy.
    generate_strategy_column():
        Generates the strategy column in the data DataFrame.
    generate_signals():
        Generates trading signals based on the momentum strategy.
    """
    def __init__(self, data, lookback_period=60, long_momentum = 0, short_momentum = 0):
        """
        Constructs all the necessary attributes for the MomentumStrategy object.

        Parameters
        ----------
            data : pandas.DataFrame
                market data
            lookback_period : int, optional
                lookback period for calculating momentum (default is 60)
            long_momentum : int or float, optional
                threshold for long momentum (default is 0)
            short_momentum : int or float, optional
                threshold for short momentum (default is 0)
        """
        self.validate_inputs(lookback_period, long_momentum, short_momentum)
        self.data = data.copy()
        self.lookback_period = lookback_period
        self.long_momentum = long_momentum
        self.short_momentum = short_momentum
        self.logger = logging.getLogger(__name__)
        self.generate_strategy_column()
    
    def validate_inputs(self, lookback_period, long_momentum, short_momentum):
        """
        Validates the inputs for the strategy.

        Parameters
        ----------
            lookback_period : int
                lookback period for calculating momentum
            long_momentum : int or float
                threshold for long momentum
            short_momentum : int or float
                threshold for short momentum

        Raises
        ------
            ValueError
                If lookback_period is not a positive integer
                If long_momentum is not an integer or float
                If short_momentum is not an integer or float
        """
        if not isinstance(lookback_period, int) or lookback_period <= 0:
            raise ValueError("lookback_period must be a positive integer")
        if not isinstance(long_momentum, int) or isinstance(long_momentum, float):
            raise ValueError("long_momentum must be an integer or float")
        if not isinstance(short_momentum, int) or isinstance(short_momentum, float):
            raise ValueError("short_momentum must be an integer or float")
    
    def generate_strategy_column(self):
        """
        Generates the strategy column in the data DataFrame.

        Returns
        -------
        pandas.DataFrame
            The updated DataFrame with the strategy column.
        """
        self.data['close_shifted'] = self.data['close'].shift(self.lookback_period)
        self.data['strategy'] = self.data['close'] - self.data['close_shifted']
        self.data.dropna(axis=0, inplace=True)
        return self.data
    
    def generate_signals(self):
        """
        Generates trading signals based on the momentum strategy.

        Returns
        -------
        list
            A list of trading signals.
        """
        signals = []
        trade_dict = {}
        prev_momentum = 0
        open_position = False
        
        for i in range(0, self.data.shape[0]):
            index = self.data.index[i]
            momentum = self.data.loc[index, 'strategy']
            if open_position == False:
                if momentum > self.long_momentum and prev_momentum <= self.long_momentum:
                    trade_dict["action"] = 'long'
                    trade_dict["open_date"] = index
                    open_position = True
                elif momentum < self.short_momentum and prev_momentum >= self.short_momentum:
                    trade_dict["action"] = 'short'
                    trade_dict["open_date"] = index
                    open_position = True
            else:
                if trade_dict["action"] == 'long' and momentum < self.long_momentum and prev_momentum >= self.long_momentum:
                    trade_dict["close_date"] = index
                    signals.append(trade_dict)
                    trade_dict = {}
                    open_position = False
                elif trade_dict["action"] == 'short' and momentum > self.short_momentum and prev_momentum <= self.short_momentum:
                    trade_dict["close_date"] = index
                    signals.append(trade_dict)
                    trade_dict = {}
                    open_position = False
            prev_momentum = momentum
        return signals

if __name__ == '__main__':
    from data_handler import DataHandler
    handler = DataHandler()
    data = handler.fetch_data(ticker="AAPL", start_date="2022-12-01", end_date="2023-12-01", add_all_technical_indicator=False)
    momentum_strategy = MomentumStrategy(data, lookback_period=60,long_momentum=2, short_momentum=-2)
    signals = momentum_strategy.generate_signals()
    print(signals)