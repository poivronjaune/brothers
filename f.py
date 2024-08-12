import tkinter as tk
from tkinter import ttk

class TreeviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview with Sorting, Filtering, and Reset")

        self.sort_column = None
        self.sort_order = 'ascending'
        
        # Create Treeview
        self.tree = ttk.Treeview(root, columns=("Column1", "Column2"), show='headings')
        self.tree.heading("Column1", text="Column 1", command=lambda: self.on_sort_column("Column1"))
        self.tree.heading("Column2", text="Column 2", command=lambda: self.on_sort_column("Column2"))

        # Original data with similar beginnings
        self.original_data = [
            ("Alice", 24),
            ("Alicia", 27),
            ("Alicia", 22),
            ("Alicea", 32),
            ("Alison", 29),
            ("Alden", 31),
            ("Albert", 26),
            ("Alvin", 30),
            ("Allen", 28),
            ("Alyssa", 25),
            ("Amanda", 23),
            ("Andy", 21),
            ("Annie", 33),
            ("Andrew", 26),
        ]

        # Insert original data into Treeview
        self.update_tree(self.original_data)

        # Pack the Treeview
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Filter entry
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", self.on_filter_change)
        self.filter_entry = tk.Entry(root, textvariable=self.filter_var, width=30)
        self.filter_entry.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset Filter", command=self.reset_filter)
        self.reset_button.pack(pady=10)

    def update_header_indicator(self, column, order):
        # Update all column headers to remove indicators
        for col in self.tree['columns']:
            self.tree.heading(col, text=col, command=lambda c=col: self.on_sort_column(c))
        
        # Update the header of the sorted column with the indicator
        if order == 'ascending':
            self.tree.heading(column, text=column + ' ↑', command=lambda: self.on_sort_column(column))
        else:
            self.tree.heading(column, text=column + ' ↓', command=lambda: self.on_sort_column(column))

    def on_sort_column(self, column):
        if self.sort_column == column:
            self.sort_order = 'descending' if self.sort_order == 'ascending' else 'ascending'
        else:
            self.sort_column = column
            self.sort_order = 'ascending'

        sorted_items = sorted(self.tree.get_children(), key=lambda item: self.tree.item(item, 'values')[self.tree['columns'].index(column)], reverse=(self.sort_order == 'descending'))
        for item in sorted_items:
            self.tree.move(item, '', 'end')

        self.update_header_indicator(column, self.sort_order)

    def on_filter_change(self, *args):
        filter_text = self.filter_var.get().lower()
        filtered_data = [item for item in self.original_data if str(item[0]).lower().startswith(filter_text)]
        
        self.update_tree(filtered_data)

    def update_tree(self, data):
        self.tree.delete(*self.tree.get_children())
        for item in data:
            self.tree.insert('', 'end', values=item)

    def reset_filter(self):
        self.filter_var.set('')  # Clear the filter text
        self.on_filter_change()  # Restore all data

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeviewApp(root)
    root.mainloop()
