import tkinter as tk
from tkinter import ttk

# Setup Root window as 1x1 empty grid
root = tk.Tk()
root.title("FOCUS")
root.geometry('800x600')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

print("Root Window created")
