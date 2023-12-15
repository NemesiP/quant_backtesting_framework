import yfinance as yf
import ta
import pandas as pd

class DataHandler:
    def __init__(self):
        # Initialization, if needed
        pass

    def fetch_data(self, 
                   ticker:str, 
                   start_date:str, 
                   end_date:str, 
                   use_path:bool=False,
                   custom_filepath:str=None,
                   frequency:str='1T',
                   interval:str='1d',
                   adjust_dataframe:bool=True,
                   add_all_technical_indicator:bool=True) -> pd.DataFrame:
        """
        Fetch historical data for a given ticker from start_date to end_date.
        """
        if use_path:
            data = self.load_custom_data(custom_filepath, 
                                         start_date, 
                                         end_date)
            if adjust_dataframe:
                data = self.preprocess_data(data, 
                                            frequency=frequency)
        else:
            data = yf.download(ticker, 
                            start=start_date, 
                            end=end_date,
                            interval=interval,
                            auto_adjust=True)
            data = self.lower_column_names(data)
            
        if add_all_technical_indicator:
            data = self.add_all_technical_indicator(data)
            
        return data

    def load_custom_data(self, 
                         custom_filepath:str, 
                         start_date:str, 
                         end_date:str) -> pd.DataFrame:
        """
        Load custom data from a CSV file.
        """
        data = pd.read_csv(custom_filepath)
        data = self.lower_column_names(data)
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        data = data.loc[start_date:end_date]
        data.sort_values(by='date', ascending=True, inplace=True)
        data = data.dropna()
        return data

    def preprocess_data(self, data, frequency:str='1T'):
        """
        Preprocess the data (e.g., handle missing values, adjust for corporate actions).
        """
        # Implement preprocessing steps here
        data = data.resample(frequency).ffill()
        return data

    def add_all_technical_indicator(self, data):
        """
        Add technical indicators to the data.
        """
        # Implement technical indicator logic here
        data = ta.add_all_ta_features(data, 
                                      open="open", 
                                      high="high", 
                                      low="low",
                                      close="close", 
                                      volume="volume")
        return data
    

    @staticmethod
    def lower_column_names(data):
        data.columns = [x.lower() for x in data.columns]
        return data
    
# Example Usage
if __name__ == "__main__":
    handler = DataHandler()
    historical_data = handler.fetch_data("AAPL", "2020-01-01", "2021-01-01")
    print(historical_data)
