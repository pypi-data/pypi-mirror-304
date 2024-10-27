"""
A class to access Kraken's zipped file
so that there is no need to unzip it (saves hard drive space).


USAGE:



# Enter path to the Kraken zip file:

DATA_PATH = os.path.expanduser("~/Downloads/Kraken_OHLCVT.zip")

# load it

kd = KrakenDataHandler(DATA_PATH)


# you can inspect which symbols it contains:
kd.list_symbols()

# when searching for a specific symbol, search with either "starts_with=" or "contains="
kd.list_symbols(starts_with="ETH")

# then get the timeframe from the specific symbol
df = kd.load_symbol_data("ETHUSDT", "15m")

# save a timreframe of a specific symbol as df pickle:
kd.save_to_df_pickle(symbol="ETHUSDT", timeframe="15m", outpath=os.path.expanduser("~/projects/python/LotusBot/src/backtester/ETHUSDT_15m.csv"), dropna_rows=True)
"""


import zipfile
import pandas as pd
import re  # For regular expression matching
import os  # to be able to use "~" for home
import platform # to distinguish MacOS

class KrakenDataHandler:

    """
    A class to handle data contained in a zipped file from Kraken exchange without the need
    to unzip the entire file, aiming to save hard disk space. This class provides functionality
    to list available trading symbols, load specific symbol data into a pandas DataFrame, and
    save symbol data as a DataFrame pickle for further analysis or backtesting.

    Attributes:
        data_zipfile (str): The path to the zipped OHLCVT data file from Kraken.
        use_old_pattern (bool): Old pattern r'^Kraken_OHLCVT/(.*)_(?P<timeframe>\d+)\.csv$' has to be used?
    
    Methods:
        list_symbols(starts_with=None, contains=None): Lists the trading symbols available in the zip file.
        load_symbol_data(symbol, timeframe): Loads OHLCVT data for a specified symbol and timeframe into a DataFrame.
        save_to_df_pickle(symbol, timeframe, outpath, dropna_rows=True): Saves the OHLCVT data for a specified symbol and timeframe into a DataFrame pickle.
        unix_to_datetime(unixtimestamp): Convert unix time (index of load_symbol_data data frame) into human-readable datetime object.
    """

    def __init__(self, data_zipfile):
        
        """
        Initializes the KrakenDataHandler with a path to a zipped data file.

        Parameters:
            data_zipfile (str): The path to the zipped file containing OHLCVT data.
        """
        
        self.data_zipfile = data_zipfile
        self.old_symbol_pattern = re.compile(r'^Kraken_OHLCVT/(.*)_(?P<timeframe>\d+)\.csv$')
        self.symbol_pattern = re.compile(r'^(.*)_(?P<timeframe>\d+)\.csv$')

    def list_symbols(self, starts_with=None, contains=None):
        """
        Lists trading symbols contained in the zip file that optionally start with a specified string or contain a specified substring.

        Parameters:
            starts_with (str, optional): Filter symbols that start with this string. Defaults to None.
            contains (str, optional): Filter symbols that contain this substring. Defaults to None.

        Returns:
            list: A sorted list of unique symbols that meet the filtering criteria.
        """


        symbols = []
        with zipfile.ZipFile(self.data_zipfile) as zip_ref:
            for filename in zip_ref.namelist():
                if filename.startswith("Kraken_OHLCVT"):
                    match = self.old_symbol_pattern.match(filename)
                    self.use_old_pattern = True
                else:
                    match = self.symbol_pattern.match(filename)
                    self.use_old_pattern = False
                if match:
                    symbol = match.group(1)
                    if (starts_with is None or symbol.startswith(starts_with)) and \
                       (contains is None or contains in symbol):
                        symbols.append(symbol)
        return sorted(set(symbols))

    def get_timeframe_mins(self, timeframe_str):
        """
        Helper function to transform timeframe string to minutes.

        Args:
            timeframe_str (_type_): _description_

        Returns:
            _type_: _description_
        """
        timeframe_map = {'1m': 1, '15m': 15, '1h': 60, '1d': 1440}
        return timeframe_map.get(timeframe_str, None)

    def load_symbol_data(self, symbol, timeframe, with_date_col=False):
        """
        Loads the OHLCVT data for a specified symbol and timeframe from the zipped file into a pandas DataFrame.
        The timestamps are Unix timestamps.
	
        Parameters:
            symbol (str): The trading symbol to load data for.
            timeframe (str): The timeframe for the data, e.g., '15m' for 15 minutes.
            with_date_col (bool): Add human readable date column? Note then the data frame is not a pure numeric table!
        
        Returns:
            DataFrame: A pandas DataFrame containing the OHLCVT data.

        Raises:
            ValueError: If the specified timeframe is not supported.
        """
        timeframe_mins = self.get_timeframe_mins(timeframe)
        if timeframe_mins is None:
            if type(timeframe) is int:
                df = self.load_resampling(symbol, timeframe)

        if self.use_old_pattern:
            filename = f"Kraken_OHLCVT/{symbol}_{timeframe_mins}.csv"
        else:
            filename = f"{symbol}_{timeframe_mins}.csv"
        with zipfile.ZipFile(self.data_zipfile) as zip_ref:
            with zip_ref.open(filename) as csvfile:
                df = pd.read_csv(csvfile, header=None, index_col=0,
                                 names=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'T'])
                
                if with_date_col: # convert Unix timestamps to datetime objects
                    df['Date'] = pd.to_datetime(df.index, unit='s').tz_localize('UTC')
                
                return df
    
    def save_to_df_pickle(self, symbol, timeframe, outpath=None, dropna_rows=True):
        """
        Saves the OHLCVT data for a specified symbol and timeframe into a DataFrame pickle file.

        Parameters:
            symbol (str): The trading symbol to save data for.
            timeframe (str): The timeframe of the data to save, e.g., '15m' for 15 minutes.
            outpath (str): The output path for the saved DataFrame pickle.
            dropna_rows (bool, optional): If True, drop rows with NaN values before saving. Defaults to True.
        """
        df = self.load_symbol_data(symbol, timeframe)
        if dropna_rows:
            df.dropna(inplace=True)
        if not outpath:
            outpath = f"{symbol}_{timeframe}.csv"
        df.to_pickle(outpath)
        
    def unix_to_datetime(self, unixtimestamp):
        """
        Converts unix time to human-dreadable datetime (Krakenohlcvt data frame index is unix time).
        
        Parameters:
            unixtimestamp (str): Kraken OHLCVT retrieved dataframes have unix time in their index. You can however give df.index as argument (faster)
        """
        return pd.to_datetime(unixtimestamp, unit='s').tz_localize('UTC')

    def load_resampling(self, symbol, timeframe, agg_dict=None):
        """
        Load and resample 1-minute interval data to a specified timeframe (given in minutes).

        Parameters:
        - df: DataFrame to resample, indexed by datetime.
        - timeframe: Desired new resampled timeframe as minutes (in int).
        - agg_dict: Dictionary specifying how to aggregate each column. If None, defaults will be used.

        Returns:
        - Resampled DataFrame.

        Usage:
          print(resample_dataframe("ETHUSDT", 30))
        """
        df = self.load_symbol_data(symbol, "1m", True)
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index, unit='s')  # Ensure index is in datetime format if it's not already
        # Default aggregation methods if not specified
        if agg_dict is None:
            agg_dict = {
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }
        
        # Return resampled and aggregated the DataFrame
        resampled_df = df.resample(timeframe).agg(agg_dict).dropna()
        # df.index is still in datetime format but should be re-transformed to unix time
        return resampled_df

