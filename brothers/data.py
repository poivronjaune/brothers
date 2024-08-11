import json
import pandas as pd
import yfinance as yf
import json
from datetime import datetime

class Data:
    '''
    Data Class contains 4 attributes:
    - tickers_df : Dataframe with symbols, Names and Url ["Symbol", "Name", "YahooTicker", "Url"]
    - tickers : List of unique symbols from the YahooTicker column
    - hist_data : Dataframe containing Dates, Symbols and OHCLV data 
    - all_dates : List of unique dates in the loaded dataset (multiple symbols per date)

    1) Initialize a Data instance
    2) Get ticker symbols [get_tickers_default(), get_tickers_from_github()]
    3) Load data [Load_data_from_yahoo(tickers), load_data_from_csv(filename)]
       Note: loading data, must adjust all attributes
    '''

    def __init__(self):
        self.tickers_df = None
        self.tickers = None
        self.hist_data = None
        self.all_dates = None
           
    def __str__(self):
        res = self.__json__()
        return f'Number of tickers: {res["tickers_len"]}, historical_data: {res["hist_data_len"]}, all_dates: {res["all_dates_len"]}'

    def __json__(self):
        tickers_len = 0 if self.tickers_df is None else len(self.tickers_df)
        hist_data_len = 0 if self.hist_data is None else len(self.hist_data)
        all_dates_len = 0 if self.all_dates is None else len(self.all_dates)
        return {"tickers_len":tickers_len, "hist_data_len":hist_data_len, "all_dates_len":all_dates_len}
    
    def get_tickers_default(self) -> pd.DataFrame:
        data = [
            # Symbol, Company Name, YahooTicker, Url
            ('IBM', 'International Business Machines Corp', 'IBM', 'https://www.advfn.com/stock-market/NYSE/IBM/stock-price'),
            ('ADBE', 'Adobe Inc', 'ADBE', 'https://www.advfn.com/stock-market/NASDAQ/ADBE/stock-price'),
            ('AMD', 'Advanced Micro Devices Inc', 'AMD', 'https://www.advfn.com/stock-market/NASDAQ/AMD/stock-price'),
            ('GOOG', 'Alphabet Inc', 'GOOG', 'https://www.advfn.com/stock-market/NASDAQ/GOOG/stock-price'),
            ('AAPL', 'Apple Inc', 'AAPL', 'https://www.advfn.com/stock-market/NASDAQ/AAPL/stock-price'),
            ('AMAT', 'Applied Materials Inc', 'AMAT', 'https://www.advfn.com/stock-market/NASDAQ/AMAT/stock-price'),
            ('AVGO', 'Broadcom Inc', 'AVGO', 'https://www.advfn.com/stock-market/NASDAQ/AVGO/stock-price'),
            ('CSCO', 'Cisco Systems Inc', 'CSCO', 'https://www.advfn.com/stock-market/NASDAQ/CSCO/stock-price'),
            ('NFLX', 'Netflix Inc', 'NFLX', 'https://www.advfn.com/stock-market/NASDAQ/NFLX/stock-price'),
            ('NVDA', 'NVIDIA Corporation', 'NVDA', 'https://www.advfn.com/stock-market/NASDAQ/NVDA/stock-price'),
            ('QCOM', 'QUALCOMM Inc', 'QCOM', 'https://www.advfn.com/stock-market/NASDAQ/QCOM/stock-price'),
            ('TXN', 'Texas Instruments Incorporated', 'TXN', 'https://www.advfn.com/stock-market/NASDAQ/TXN/stock-price'),
            ('ZDGE', 'Zedge Inc', 'ZDGE', 'https://www.advfn.com/stock-market/AMEX/ZDGE/stock-price')
        ]
        
        tickers_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'YahooTicker', 'Url'])
        return tickers_df

    def get_tickers_from_github(self) -> pd.DataFrame:
        # Github symbols list (should be valid symbols)
        # Headers : Symbol, Name, YahooTicker, Url   (We need to keep the YahooTicker column)
        url1 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_tsx.csv'
        url2 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_nyse.csv'
        url3 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_nasdaq.csv'
        url4 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_amex.csv'

        # tickers_df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'YahooTicker', 'Url'])
        tickers_df = pd.read_csv(url1)
        tickers_df = pd.concat([tickers_df, pd.read_csv(url2)])
        tickers_df = pd.concat([tickers_df, pd.read_csv(url3)])
        tickers_df = pd.concat([tickers_df, pd.read_csv(url4)])
        tickers_df = tickers_df.drop_duplicates(subset=['Symbol', 'YahooTicker'])

        return tickers_df

    
    def load_data_from_yahoo(self, tickers_df, start_dt='2020-01-01'):
        tickers = tickers_df.YahooTicker.to_list() 

        hist_data = yf.download(tickers, start=start_dt, end=datetime.now())
        hist_data = hist_data.stack().reset_index()
        hist_data.columns = ['Datetime', 'Symbol', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
        hist_data.Datetime = pd.to_datetime(hist_data.Datetime)
        hist_data.Datetime = hist_data.Datetime.dt.strftime('%Y-%m-%d %H:%M:%S')
        
        self.hist_data = hist_data
        self.all_dates = self.hist_data.Datetime.unique().tolist()
        self.tickers = self.hist_data.Symbol.unique().tolist()
        self.tickers_df = tickers_df


    def load_data_from_csv(self, filename='V1--hist_data_2024-07-31.csv'):
        data = pd.read_csv(filename, index_col=False)
        required_columns = ['Datetime','Symbol','Adj Close','Close','High','Low','Open','Volume']
        if set(required_columns).issubset(data.columns):
            self.hist_data = data
            self.all_dates = self.hist_data.Datetime.unique().tolist()
            self.tickers = self.hist_data.Symbol.unique()
            self.tickers_df = pd.DataFrame(self.tickers, columns=['Symbol'])
            self.tickers_df["Company Name"] = "Not loaded"
            self.tickers_df["YahooTicker"] = self.tickers
            self.tickers_df["Url"] = "Not loaded"
        else:
            self.hist_data = None
            self.all_dates = None
            self.tickers = None
            self.tickers_df = None


    def save_data(self, filename="historical_data.csv"):
        self.hist_data.to_csv(filename, index=False)