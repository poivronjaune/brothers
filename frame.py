import tkinter as tk
from tkinterweb import HtmlFrame

# Create the main window
root = tk.Tk()
root.title("Webpage Viewer")
root.geometry("800x600")

# Create the HtmlFrame (the browser frame)
frame = HtmlFrame(root)

# Load a webpage
frame.load_website("https://robertboivin.ca/")

# Pack the frame into the window
frame.pack(fill="both", expand=True)

# Start the Tkinter event loop
root.mainloop()
