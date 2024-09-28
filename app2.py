import sys
import pandas as pd
import yfinance as yf
from datetime import date, datetime

#from flask import Flask, render_template, request
#import threading

from brothers.windows import MainWindow
from brothers.webframe import WebFrame
from brothers.data import Data


if __name__ == '__main__':    
    web_frame = WebFrame()
    data_obj = Data()

    #list_of_tickers_to_load_df = data_obj.get_tickers_from_github()
    #data_obj.load_data_from_yahoo(tickers_df=list_of_tickers_to_load_df)
    #data_obj.save_data(filename='daily-2020-2024.csv')
    
    data_obj.load_data_from_csv(filename='daily-2020-2024.csv')
    #print(f'{data_obj.hist_data}')
    #print(data_obj.tickers_df)

    display = MainWindow(data_obj.tickers_df, data_obj.hist_data)
    display.show()
