from datetime import datetime, timedelta
from flask import Flask, render_template

import pandas as pd
import threading
import webbrowser
import json
from lightweight_charts import Chart

def fake_data():
    data = [
            ["Symbol","Close","High","Low","Open","Volume","Datetime","Adj Close"],
            ["ORRF",21, 21, 21, 21, 0   ,"2023-03-13",21.709999084472],
            ["ORRF",21, 21, 21, 21, 333 ,"2023-03-14",21.709999084472],
            ["ORRF",22, 22, 22, 22, 197 ,"2023-03-15",22.092500686645],
            ["ORRF",22, 22, 22, 22, 284 ,"2023-03-16",22.112499237060],
            ["ORRF",22, 22, 22, 22, 426     ,"2023-03-17",22.0],
            ["ORRF",21, 21, 21, 21, 723 ,"2023-03-20",21.780000686645],
            ["ORRF",21, 21, 21, 21, 910 ,"2023-03-21",21.709999084472],
            ["ORRF",21, 21, 21, 21, 370 ,"2023-03-22",21.659999847412],
            ["ORRF",21, 21, 21, 21, 416 ,"2023-03-23",21.370000839233],
            ["ORRF",21, 21, 21, 21, 394 ,"2023-03-24",21.409999847412],
            ["ORRF",21, 21, 21, 21, 156 ,"2023-03-21",21.240900039672],
            ["ORRF",21, 21, 21, 21, 841     ,"2023-03-22",21.200000762939],
            ["ORRF",21, 21, 20, 20, 909 ,"2023-03-23",21.180000305175],
            ["ORRF",20, 20, 20, 20, 645     ,"2023-03-24",20.799999237060],
            ["ORRF",20, 20, 20, 20, 365   ,"2023-03-27",20.780000686645],
            ["ORRF",20, 20, 20, 20, 532    ,"2023-03-28",20.799999237060],
            ["ORRF",20, 20, 20, 20, 335  ,"2023-03-29",20.799999237060],
            ["ORRF",20, 20, 20, 20, 420 ,"2023-03-30",20.809999465942],
            ["ORRF",20, 20, 20, 20, 848 ,"2023-03-31",20.809999465942]
        ]

    df = pd.DataFrame(data[1:], columns=data[0])
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.drop(columns='Adj Close', inplace=True)
    #df.set_index('Datetime', inplace=True)    
    return df  

class LightWeightChart:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.app = Flask(__name__, static_folder='static', template_folder='templates')
        
        @self.app.route('/tmp')
        def index():
            # Prepare data for the chart
            chart_data = self.df.apply(lambda row: {
                #'time': row['Datetime'].strftime('%Y-%m-%dT%H:%M:%S'),
                'time': row['Datetime'].strftime('%Y-%m-%d'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
            }, axis=1).tolist()
            print(chart_data)
            return render_template('chart.html', chart_data=json.dumps(chart_data))
            #return render_template('chart.html', chart_data=chart_data)

        @self.app.route('/')
        def demo():
            return render_template('home.html')

    def open_browser(self):
        webbrowser.open_new('http://127.0.0.1:5000/')
        
    def run(self):
        

        # Run Flask app
        self.app.run(debug=False)
        

if __name__ == '__main__':
    df = fake_data()
    df = df[['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]   
    df.reset_index()
    chart = LightWeightChart(df)
    chart.run()    


class TVChart():
    def __init__(self, data_df, maximize=False):
        self.chart_object = Chart(maximize=maximize, toolbox=True)
        self.data = None
        self.test = 'Class initiated...'
        self.symbol = ''
        self.set_data(data_df)

    def __str__(self):
        return self.test

    def set_data(self, data_df):
        if not isinstance(data_df, pd.DataFrame):
            raise ValueError('Not a DataFrame.')
        if len(data_df) < 1:
            raise ValueError('Not enough data points to print chart')
        self.data = data_df
        self.symbol = data_df.iloc[0]["Symbol"]
        self.chart_object.set(self.data)

    def show(self):
        self.chart_object.topbar.textbox('symbol', self.symbol)
        self.chart_object.watermark(self.symbol)
        self.chart_object.legend(visible=True, ohlc=True, percent=False, font_size=14)
        self.chart_object.show(block=True)
#         
# 
# 
# def fake_data():
#     data = [
#             ["Symbol","Close","High","Low","Open","Volume","Datetime","Adj Close"],
#             ["ORRF",21.71,21.71,21.71,21.71,0,"2023-03-13T09:30:00.000000Z",21.709999084472],
#             ["ORRF",21.71,21.71,21.71,21.71,333,"2023-03-13T09:31:00.000000Z",21.709999084472],
#             ["ORRF",22.09,22.09,22.09,22.09,197,"2023-03-13T09:58:00.000000Z",22.092500686645],
#             ["ORRF",22.11,22.11,22.11,22.11,284,"2023-03-13T10:00:00.000000Z",22.112499237060],
#             ["ORRF",22.0,22.0,22.0,22.0,426,"2023-03-13T10:41:00.000000Z",22.0],
#             ["ORRF",21.78,21.78,21.78,21.78,723,"2023-03-13T10:53:00.000000Z",21.780000686645],
#             ["ORRF",21.71,21.79,21.71,21.79,910,"2023-03-13T10:54:00.000000Z",21.709999084472],
#             ["ORRF",21.66,21.66,21.66,21.66,370,"2023-03-13T12:41:00.000000Z",21.659999847412],
#             ["ORRF",21.37,21.37,21.37,21.37,416,"2023-03-13T12:47:00.000000Z",21.370000839233],
#             ["ORRF",21.41,21.41,21.41,21.41,394,"2023-03-13T13:00:00.000000Z",21.409999847412],
#             ["ORRF",21.24,21.24,21.24,21.24,156,"2023-03-13T13:11:00.000000Z",21.240900039672],
#             ["ORRF",21.2,21.2,21.2,21.2,841,"2023-03-13T13:18:00.000000Z",21.200000762939],
#             ["ORRF",21.18,21.18,20.95,20.95,909,"2023-03-13T13:32:00.000000Z",21.180000305175],
#             ["ORRF",20.8,20.9,20.8,20.8,645,"2023-03-13T13:47:00.000000Z",20.799999237060],
#             ["ORRF",20.78,20.8,20.78,20.8,365,"2023-03-13T13:52:00.000000Z",20.780000686645],
#             ["ORRF",20.8,20.8,20.78,20.8,532,"2023-03-13T14:03:00.000000Z",20.799999237060],
#             ["ORRF",20.8,20.81,20.79,20.79,335,"2023-03-13T14:11:00.000000Z",20.799999237060],
#             ["ORRF",20.81,20.83,20.81,20.83,420,"2023-03-13T14:26:00.000000Z",20.809999465942],
#             ["ORRF",20.81,20.81,20.81,20.81,848,"2023-03-13T14:27:00.000000Z",20.809999465942],
#             ["ORRF",20.81,20.81,20.81,20.81,730,"2023-03-13T14:29:00.000000Z",20.809999465942],
#             ["ORRF",21.19,21.19,21.0,21.0,980,"2023-03-13T15:06:00.000000Z",21.189899444580],
#             ["ORRF",20.99,20.99,20.99,20.99,110,"2023-03-13T15:16:00.000000Z",20.985000610351],
#             ["ORRF",20.86,20.86,20.86,20.86,819,"2023-03-13T15:21:00.000000Z",20.860000610351],
#             ["ORRF",20.53,20.56,20.53,20.56,310,"2023-03-13T15:34:00.000000Z",20.531600952148],
#             ["ORRF",20.42,20.84,20.42,20.84,423,"2023-03-13T15:57:00.000000Z",20.420000076293],
#             ["ORRF",20.41,20.44,20.36,20.44,1079,"2023-03-13T15:59:00.000000Z",20.409999847412],
#             ["ORRF",21.76,21.76,21.76,21.76,0,"2023-03-14T09:30:00.000000Z",21.760000228881],
#             ["ORRF",21.42,21.42,21.34,21.34,457,"2023-03-14T09:59:00.000000Z",21.424999237060]
#         ]
# 
#     df = pd.DataFrame(data[1:], columns=data[0])
#     df['Datetime'] = pd.to_datetime(df['Datetime'])
#     df.set_index('Datetime', inplace=True)    
#     return df   
# 
# if __name__ == '__main__':
#     data1_df = fake_data()
#     c1 = TVChart(data1_df)
#     #print(data1_df)
#     c1.show()

