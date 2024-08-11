import json
import pandas as pd
import yfinance as yf
import json
from datetime import datetime

class Data:
    def __init__(self, load=False):
        self.tickers_df = None
        self.tickers = self.default_tickers()
        self.hist_data = None
        self.all_dates = None

        if load:
            self.hist_data = self.load_data_from_yfinance(self.tickers)
            self.all_dates = self.hist_data.Datetime.unique().tolist()
            

    def __str__(self):
        #tickers_len = len(self.tickers)
        #hist_data_len = 0 if self.hist_data == None else len(self.hist_data)
        #all_dates_len = 0 if self.all_dates == None else len(self.all_dates)
        #return f'Number of tickers: {tickers_len}, historical_data:{hist_data_len}, all_dates: {all_dates_len}'

        res = self.__json__()
        return f'Number of tickers: {res["tickers_len"]}, historical_data: {res["hist_data_len"]}, all_dates: {res["all_dates_len"]}'

    def __json__(self):
        tickers_len = len(self.tickers)
        hist_data_len = 0 if self.hist_data == None else len(self.hist_data)
        all_dates_len = 0 if self.all_dates == None else len(self.all_dates)
        return {"tickers_len":tickers_len, "hist_data_len":hist_data_len, "all_dates_len":all_dates_len}
    
    def default_tickers(self):
        data = [
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
        self.tickers_df = pd.DataFrame(data, columns=['Ticker', 'Company Name', 'Symbol', 'Url'])
        tickers = self.tickers_df.Symbol.unique().tolist()
        return tickers

    def load_tickers_from_github(self):
        # Github symbols list (should be valid symbols)
        url1 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_tsx.csv'
        url2 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_nyse.csv'
        url3 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_nasdaq.csv'
        url4 = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO2024/yahoo_amex.csv'

        tickers_df = pd.read_csv(url1)
        tickers_df = pd.concat([tickers_df, pd.read_csv(url2)])
        tickers_df = pd.concat([tickers_df, pd.read_csv(url3)])
        tickers_df = pd.concat([tickers_df, pd.read_csv(url4)])
        tickers_df = tickers_df.drop_duplicates(subset=['Symbol', 'YahooTicker'])

        tickers = tickers_df.YahooTicker.to_list() 
        
        self.tickers = tickers 
        return self.tickers  

    def load_data_from_yfinance(self, tickers, start_dt='2020-01-01'):
        hist_data = yf.download(tickers, start=start_dt, end=datetime.now())
        hist_data = hist_data.stack().reset_index()
        hist_data.columns = ['Datetime', 'Ticker', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
        hist_data.Datetime = pd.to_datetime(hist_data.Datetime)
        hist_data.Datetime = hist_data.Datetime.dt.strftime('%Y-%m-%d %H:%M:%S')
        
        self.hist_data = hist_data
        self.all_dates = self.hist_data.Datetime.unique().tolist()

    def load_data_from_csv(self, filename='V1--hist_data_2024-07-31.csv'):
        # TODO: Fix this file load to compare with loaded_tickers? Need a tickers_df with Company names and Url...
        data = pd.read_csv(filename, index_col=False)
        required_columns = ['Datetime','Ticker','Adj Close','Close','High','Low','Open','Volume']
        if set(required_columns).issubset(data.columns):
            self.hist_data = data
            self.all_dates = self.hist_data.Datetime.unique().tolist()
        else:
            self.hist_data = None
            self.all_dates = None


    def save_data(self, filename="historical_data.csv"):
        self.hist_data.to_csv(filename, index=False)