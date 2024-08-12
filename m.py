import tkinter as tk
from tkinter import ttk

class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Viewer")

        # Master Treeview for Stock Symbols
        self.master_tree = ttk.Treeview(self, columns=("Symbol",), show="headings")
        self.master_tree.heading("Symbol", text="Stock Symbol")
        self.master_tree.bind("<<TreeviewSelect>>", self.on_stock_select)
        self.master_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Detail Treeview for Historical Prices
        self.detail_tree = ttk.Treeview(self, columns=("Date", "Price"), show="headings")
        self.detail_tree.heading("Date", text="Date")
        self.detail_tree.heading("Price", text="Price")
        self.detail_tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sample data
        self.stock_data = {
            "AAPL": [("2024-08-01", "180.00"), ("2024-08-02", "182.00"), ("2024-08-03", "181.50")],
            "GOOGL": [("2024-08-01", "2700.00"), ("2024-08-02", "2720.00"), ("2024-08-03", "2715.00")],
            "MSFT": [("2024-08-01", "310.00"), ("2024-08-02", "315.00"), ("2024-08-03", "312.50")]
        }

        # Populate master treeview with stock symbols
        for symbol in self.stock_data.keys():
            self.master_tree.insert("", tk.END, values=(symbol,))

    def on_stock_select(self, event):
        selected_item = self.master_tree.selection()[0]
        selected_stock = self.master_tree.item(selected_item, "values")[0]

        # Clear the detail treeview
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)

        # Insert the historical prices for the selected stock
        for date, price in self.stock_data[selected_stock]:
            self.detail_tree.insert("", tk.END, values=(date, price))

if __name__ == "__main__":
    app = StockApp()
    app.geometry("600x400")
    app.mainloop()
