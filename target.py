import tkinter as tk
from tkinter import ttk
import webbrowser
from flask import Flask, render_template, request
import threading

app = Flask(__name__)

# Sample data
stock_data = [
    ("AW.UN", "A and W Revenue Royalties Income Fund", "AW-UN.TO", "https://www.advfn.com/stock-market/TSX/AW.UN/stock-price"),
    ("AAB", "Aberdeen International Inc", "AAB.TO", "https://www.advfn.com/stock-market/TSX/AAB/stock-price"),
    ("FAP", "Abrdn Asia Pacific Income Fund VCC", "FAP.TO", "https://www.advfn.com/stock-market/TSX/FAP/stock-price"),
    ("ADN", "Acadian Timber Corp", "ADN.TO", "https://www.advfn.com/stock-market/TSX/ADN/stock-price"),
    ("ACD", "Accord Financial Corporation", "ACD.TO", "https://www.advfn.com/stock-market/TSX/ACD/stock-price"),
    ("ARA", "Aclara Resources Inc", "ARA.TO", "https://www.advfn.com/stock-market/TSX/ARA/stock-price"),
    ("ADCO", "Adcore Inc", "ADCO.TO", "https://www.advfn.com/stock-market/TSX/ADCO/stock-price"),
    ("ADEN", "Adentra Inc", "ADEN.TO", "https://www.advfn.com/stock-market/TSX/ADEN/stock-price")
]

# Flask route to display stock details
@app.route('/chart_view')
def chart_view():
    symbol = request.args.get('symbol')
    name = request.args.get('name')
    yahoo_ticker = request.args.get('yahoo_ticker')
    url = request.args.get('url')
    return render_template('chart_view.html', symbol=symbol, name=name, yahoo_ticker=yahoo_ticker, url=url)

# Function to start Flask server
def start_flask_app():
    app.run(debug=True, use_reloader=False)

# Tkinter App class
class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Viewer")
        
        # Create Treeview
        self.tree = ttk.Treeview(self, columns=("Symbol", "Name", "YahooTicker", "Url"), show='headings')
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Name", text="Name")
        self.tree.heading("YahooTicker", text="YahooTicker")
        self.tree.heading("Url", text="Url")
        
        # Insert data into the tree
        for stock in stock_data:
            self.tree.insert('', tk.END, values=stock)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind click event
        self.tree.bind("<Double-1>", self.on_tree_click)

    def on_tree_dclick(self, event):
        selected_item = self.tree.selection()[0]
        stock_info = self.tree.item(selected_item, "values")
    
    def on_tree_click(self, event):
        # Get selected item
        selected_item = self.tree.selection()[0]
        stock_info = self.tree.item(selected_item, "values")
        
        # Open the browser with Flask server URL and stock info
        url = f"http://127.0.0.1:5000/chart_view?symbol={stock_info[0]}&name={stock_info[1]}&yahoo_ticker={stock_info[2]}&url={stock_info[3]}"
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the Tkinter app
    app = StockApp()
    app.mainloop()
