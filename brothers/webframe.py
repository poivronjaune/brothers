from flask import Flask, render_template, request
import threading
import logging
import json

class WebFrame:
    def __init__(self):
        self.app = Flask(__name__)
        self.data_df = None
        
        @self.app.route('/info')
        def info():
            #symbol = 'AAPL'
            #name = 'Apple Inc.'
            #yahoo_ticker = 'AAPL'
            #url = "https://www.apple.com/"
            symbol = request.args.get('symbol')
            name = request.args.get('name')
            yahoo_ticker = request.args.get('yahoo_ticker')
            url = request.args.get('url')

            return render_template('info.html', symbol=symbol, name=name, yahoo_ticker=yahoo_ticker, url=url)
        
        @self.app.route('/demo')
        def demo():
            return render_template('demo.html')

        @self.app.route('/chart')
        def chart():
            data = request.json.get('data', [])
            return render_template('chart.html', chart_data=data)

        @self.app.route('/chart2')
        def chart2():
            title = "TradingView Chart"
            message = "Hello World!"
            
            # Sample chart data (can be dynamically loaded from a DataFrame)
            chart_data = [
                { 'open': 10, 'high': 10.63, 'low': 9.49, 'close': 9.55, 'time': 1642427876 }, 
                { 'open': 9.55, 'high': 10.30, 'low': 9.42, 'close': 9.94, 'time': 1642514276 }, 
                { 'open': 9.94, 'high': 10.17, 'low': 9.92, 'close': 9.78, 'time': 1642600676 },
                { 'open': 9.78, 'high': 10.59, 'low': 9.18, 'close': 9.51, 'time': 1642687076 },
                { 'open': 9.51, 'high': 10.46, 'low': 9.10, 'close': 10.17, 'time': 1642773476 },
                { 'open': 10.17, 'high': 10.96, 'low': 10.16, 'close': 10.47, 'time': 1642859876 },
                { 'open': 10.47, 'high': 11.39, 'low': 10.40, 'close': 10.81, 'time': 1642946276 },
                { 'open': 10.81, 'high': 11.60, 'low': 10.30, 'close': 10.75, 'time': 1643032676 },
                { 'open': 10.75, 'high': 11.60, 'low': 10.49, 'close': 10.93, 'time': 1643119076 },
                { 'open': 10.93, 'high': 11.53, 'low': 10.76, 'close': 10.96, 'time': 1643205476 }
            ]
            
            return render_template('chart.html', title=title, message=message, chart_data=json.dumps(chart_data))


        # Start Flask server in a background thread
        flask_thread = threading.Thread(target=self.start_flask_app)
        flask_thread.daemon = True
        flask_thread.start()

    def start_flask_app(self):
        self.app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    wed_frame = WebFrame()
    print('CTRL-C To quit')
    while True:
        pass