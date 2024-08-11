import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, symbols, live_data):
        self.live_data = live_data
        self.symbols = symbols
        self.root = tk.Tk()
        self.root.resizable(True, True)
        
        icon_path = "brothers/favicon.ico"
        self.root.iconbitmap(icon_path)

        self._setup_window_size()

        self.root.title("Hobby Trading")
        self.label = tk.Label(self.root, text="Hello, World!", font=("Arial", 24))
        self.label.pack(pady=20)    


    def _setup_window_size(self):
        display_width = self.root.winfo_screenwidth() 
        display_height = self.root.winfo_screenheight() 
        screen_width =  int(display_width * 0.80)
        screen_height = int(display_height * 0.80)
        self.root.geometry(f'{screen_width}x{screen_height}+10+10')

        self.root.resizable(True, True)

        self.left_frame = None
        self.right_frame = None    

    def create_data_frame(self):
        frame = tk.Frame(self.root)
        frame.pack_propagate(False)  # Prevent resizing based on contents

        # Title for the left frame
        frame_title = tk.Label(frame, text="Price Data", font=("Arial", 18, "bold"))
        frame_title.pack(fill=tk.X, padx=10, pady=(10, 0))

        data = self.live_data.groupby('Ticker').first().reset_index()
        data = data.drop(columns=['Adj Close'])

        columns_order = ['Datetime', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
        columns_width = [130, 50, 60, 60, 60, 60, 130]
        data = data[columns_order]

        tree = ttk.Treeview(frame, columns=list(data.columns), show='headings')

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

        return frame # Pack this in your layout

    def create_symbols_frame(self):
        frame = tk.Frame(self.root)
        frame.pack_propagate(False)  # Prevent resizing based on contents

        # Title for the right frame
        frame_title = tk.Label(frame, text="Symbols", font=("Arial", 18, "bold"))
        frame_title.pack(fill=tk.X, padx=10, pady=(10, 0))

        
        columns_order = ['Symbol', 'Company Name', 'Url']
        columns_width = [50, 200, 250]
        data = self.symbols[columns_order]

        #tree = ttk.Treeview(frame, columns=list(data.columns), show='headings')
        tree = ttk.Treeview(frame)
        tree['columns'] = list(data.columns)
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
            tree.insert("", "end", values=list(row))

        #label = tk.Label(frame, text="Symbols Frame")
        #label.pack(expand=True, padx=20, pady=20)

        return frame

    def assemble_window(self):
        self.frame1 = self.create_symbols_frame()
        self.frame2 = self.create_data_frame()
        

        # Layout frames in the window
        # Set both frames to take up 50% of the window width
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        

    def show(self):
        self.assemble_window()
        self.root.mainloop()