import time
import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk
import webbrowser

from brothers.chart import TVChart

class PriceGrid:
    def __init__(self, root, data_df):
        self.root = root
        self.data_df = data_df
        self.tree_grid = None
        self.frame = self.setup_frame()

    def setup_frame(self):
        frame = tk.Frame(self.root)
        frame.pack_propagate(False)  # Prevent resizing based on contents

        # Title for the left frame
        frame_title = tk.Label(frame, text="Price Data", font=("Arial", 18, "bold"))
        frame_title.pack(fill=tk.X, padx=10, pady=(10, 0))

        data = self.data_df

        columns_order = ['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
        columns_width = [130, 50, 60, 60, 60, 60, 130, 60]
        data = data[columns_order]

        #tree = ttk.Treeview(frame, columns=list(data.columns), show='headings')
        tree = ttk.Treeview(frame)
        tree['columns'] =list(data.columns)
        tree['show'] = "headings"

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill=tk.BOTH, expand=1)

        for index, col in enumerate(data.columns):
            tree.heading(col, text=col)
            tree.column(col, width=columns_width[index], stretch=False)

        for index, row in data.iterrows():
            formatted_row = [row[col] if col not in ['Open', 'High', 'Low', 'Close'] else f"{row[col]:.2f}" for col in data.columns]
            tree.insert("", "end", values=formatted_row)

        self.tree_grid = tree  # Save a reference for call back functions
        return frame # Pack this in your layout

class SymbolsGrid:
    def __init__(self, root, data_df):
        self.root = root
        self.data_df = data_df
        self.tree_grid = None
        self.sort_column = None
        self.sort_order = 'ascending'
        self.frame = self.setup_frame()

    def setup_frame(self):
        frame = tk.Frame(self.root)
        frame.pack_propagate(False)  # Prevent resizing based on contents

        # Title for the right frame
        frame_title = tk.Label(frame, text="Symbols", font=("Arial", 18, "bold"))
        frame_title.pack(fill=tk.X, padx=10, pady=(10, 0))

        data = self.data_df
        columns_order = ['Symbol', 'Name', 'YahooTicker', 'Url']
        columns_width = [50, 200, 50, 250]
        data = data[columns_order]
        data = data.sort_values(by='Symbol', ascending=True)

        tree = ttk.Treeview(frame)
        tree['columns'] = list(data.columns)
        tree['show'] = "headings"
        tree.heading(columns_order[0], text=columns_order[0], command=lambda: self.on_sort_column(columns_order[0]))

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill=tk.BOTH, expand=1)

        for index, col in enumerate(data.columns):
            tree.heading(col, text=col)
            tree.column(col, width=columns_width[index], stretch=False)

        for index, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        self.tree_grid = tree
        return frame    

    def on_sort_column(self, column):
        if self.sort_column == column:
            self.sort_order = 'descending' if self.sort_order == 'ascending' else 'ascending'
        else:
            self.sort_column = column
            self.sort_order = 'ascending'

        sorted_items = sorted(self.tree_grid.get_children(), key=lambda item: self.tree_grid.item(item, 'values')[self.tree_grid['columns'].index(column)], reverse=(self.sort_order == 'descending'))
        for item in sorted_items:
            self.tree_grid.move(item, '', 'end')

        self.update_header_indicator(column, self.sort_order)

    def update_header_indicator(self, column, order):
        # Update all column headers to remove indicators
        for col in self.tree_grid['columns']:
            self.tree_grid.heading(col, text=col, command=lambda c=col: self.on_sort_column(c))
        
        # Update the header of the sorted column with the indicator
        if order == 'ascending':
            self.tree_grid.heading(column, text=column + ' ↑', command=lambda: self.on_sort_column(column))
        else:
            self.tree_grid.heading(column, text=column + ' ↓', command=lambda: self.on_sort_column(column))



class MainWindow:
    def __init__(self, symbols_df, live_data):
        self.live_data = live_data
        self.symbols = symbols_df
        self.root = tk.Tk()
        self.root.resizable(True, True)
        
        icon_path = "brothers/favicon.ico"
        self.root.iconbitmap(icon_path)

        self._setup_window_size()

        self.root.title("Hobby Trading")
        self.label = tk.Label(self.root, text="Hello, World!", font=("Arial", 24))
        self.label.pack(pady=20)    

        self.charts = []

    def _setup_window_size(self):
        display_width = self.root.winfo_screenwidth() 
        display_height = self.root.winfo_screenheight() 
        screen_width =  int(display_width * 0.80)
        screen_height = int(display_height * 0.80)
        self.root.geometry(f'{screen_width}x{screen_height}+10+10')

        self.root.resizable(True, True)

        self.left_frame = None
        self.right_frame = None    

    def create_data_frame(self, PG):
        frame = PG.frame
        self.details_tree = PG.tree_grid
        return frame

    def create_symbols_frame(self, SG):
        frame = SG.frame
        self.symbols_tree = SG.tree_grid
        return frame

    def on_symbols_select(self, event):
        selected_item = self.symbols_tree.selection()[0]
        selected_symbol = self.symbols_tree.item(selected_item, "values")[2]

        #print(f'Symbol selected: {selected_item}, {selected_symbol}')
        
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        
        prices_df = self.live_data.query('Symbol == @selected_symbol')
        for index, row in prices_df.iterrows():
            formatted_row = [row[col] if col not in ['Open', 'High', 'Low', 'Close'] else f"{row[col]:.2f}" for col in prices_df.columns]
            self.details_tree.insert("", tk.END, values=formatted_row)

    def on_symbols_double_click(self, event):
        item = self.symbols_tree.identify_row(event.y)
        
        if item:
            # Get item details
            item_values = self.symbols_tree.item(item, "values")
            print("Double-clicked on:", item_values)
            url = f'http://127.0.0.1:5000/chart2'
            webbrowser.open(url)

            #selected_symbol = item_values[0]
            #company = item_values[1]
            #url = item_values[3]
            #data_df = self.live_data.query('Symbol == @selected_symbol').copy()
            #data_df["Datetime"] = pd.to_datetime(data_df['Datetime'])
            ##data_df.set_index('Datetime', inplace=True)
            #chart_data = data_df.apply(lambda row: {
            #    #'time': row['Datetime'].strftime('%Y-%m-%dT%H:%M:%S'),
            #    'time': row['Datetime'].strftime('%Y-%m-%d'),
            #    'open': row['Open'],
            #    'high': row['High'],
            #    'low': row['Low'],
            #    'close': row['Close'],
            #}, axis=1).tolist()

            #chart = TVChart(chart_data)
            #chart.show()
        else:
            print("No item clicked")

    def assemble_window(self):
        SG = SymbolsGrid(self.root, data_df=self.symbols)
        self.frame1 = SG.frame
        self.symbols_tree = SG.tree_grid

        selected_symbol = self.symbols.loc[0, 'YahooTicker']
        prices_df = self.live_data.query('Symbol == @selected_symbol')        
        PG = PriceGrid(self.root, data_df=prices_df)
        self.frame2 = PG.frame
        self.details_tree = PG.tree_grid
        
        # Set both frames to take up 50% of the window width
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # connect callback functions
        # tree.bind("<<TreeviewSelect>>",self.on_symbols_select)
        self.symbols_tree.bind("<<TreeviewSelect>>",self.on_symbols_select)
        self.symbols_tree.bind("<Double-Button-1>", self.on_symbols_double_click)

    def show(self):
        self.assemble_window()
        self.root.mainloop()