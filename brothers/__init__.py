from . import version

from flask import Flask, render_template
import pandas as pd
import json
import threading
import webbrowser


from brothers.data import Data
from brothers.windows import MainWindow
from brothers.chart import LightWeightChart

__version__ = version.version
__author__ = "Poivron Jaune"
__author_email__ = "poivronjaune@gmail.com"
__short_description__ = "Trading simulator for multi-asset analysis"

import warnings
warnings.filterwarnings('default', category=DeprecationWarning, module='^yfinance')

__all__ = ['download', 'Ticker', 'Tickers', 'enable_debug_mode', 'set_tz_cache_location']



#class LightWeightChart:
#    def __init__(self, df: pd.DataFrame):
#        self.df = df
#        self.app = Flask(__name__, static_folder='static', template_folder='templates')
#        
#        @self.app.route('/tmp')
#        def index():
#            # Prepare data for the chart
#            chart_data = self.df.apply(lambda row: {
#                #'time': row['Datetime'].strftime('%Y-%m-%dT%H:%M:%S'),
#                'time': row['Datetime'].strftime('%Y-%m-%d'),
#                'open': row['Open'],
#                'high': row['High'],
#                'low': row['Low'],
#                'close': row['Close'],
#            }, axis=1).tolist()
#            print(chart_data)
#            return render_template('chart.html', chart_data=json.dumps(chart_data))
#            #return render_template('chart.html', chart_data=chart_data)
#
#        @self.app.route('/')
#        def demo():
#            return render_template('demo.html')
#
#    def open_browser(self):
#        webbrowser.open_new('http://127.0.0.1:5000/')
#        
#    def run(self):
#        # Open browser in a separate thread
#        
#        threading.Timer(1, self.open_browser).start()
#        # Run Flask app
#        self.app.run(debug=True)

