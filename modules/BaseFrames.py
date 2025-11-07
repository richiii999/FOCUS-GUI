import tkinter as tk
from tkinter import ttk

class BaseFrames(tk.Frame):
    def __init__(self, master):
        super().__init__(master) # required idk

        # L Frame & Label
        self.L = tk.Frame(self, width=800, height=800, bg="grey", relief='ridge', borderwidth=5)
        self.LLabel = tk.Label(self.L, text="LLabel", bg="grey")
        
        # TR Frame & Label
        self.TR = tk.Frame(self, width=400, height=400, bg="skyblue", relief='ridge', borderwidth=5)
        self.TRLabel = tk.Label(self.TR, text="TRLabel", bg="skyblue")

        # BR Frame & Label
        self.BR = tk.Frame(self, width=400, height=400, bg="skyblue", relief='ridge', borderwidth=5)
        self.BRLabel = tk.Label(self.BR, text="BRLabel", bg="skyblue")


        ## Grid placement
        # BaseFrames is within the root grid
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)

        # L
        self.L.columnconfigure(0, weight=2)
        self.L.rowconfigure(0, weight=2)
        self.L.grid(column=0, row=0, columnspan=1, rowspan=2, sticky='news')

        self.LLabel.grid(column=0, row=0)

        # TR
        self.TR.columnconfigure(0, weight=1)
        self.TR.rowconfigure(0, weight=1)
        self.TR.grid(column=1, row=0, sticky='news')

        self.TRLabel.grid(column=0, row=0)

        # BR
        self.BR.columnconfigure(0, weight=1)
        self.BR.rowconfigure(0, weight=1)
        self.BR.grid(column=1, row=1, sticky='news')

        self.BRLabel.grid(column=0, row=0)

        self.grid(row=0, column=0, sticky='news')
