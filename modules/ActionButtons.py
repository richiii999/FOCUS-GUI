import tkinter as tk
from tkinter import ttk

class ActionButtons(tk.Frame):
    def __init__(self, master):
        # Action Buttons
        super().__init__(master)
        self.A1 = tk.Button(self, text="A1", bg="red",    relief='ridge', borderwidth=3)
        self.A2 = tk.Button(self, text="A2", bg="green",  relief='ridge', borderwidth=3)
        self.A3 = tk.Button(self, text="A3", bg="blue",   relief='ridge', borderwidth=3)
        self.A4 = tk.Button(self, text="A4", bg="yellow", relief='ridge', borderwidth=3)
        self.A5 = tk.Button(self, text="A5", bg="purple", relief='ridge', borderwidth=3)
        self.A6 = tk.Button(self, text="A6", bg="cyan",   relief='ridge', borderwidth=3)

        # Action Button default bindings
        self.A1.bind('<ButtonPress-1>', lambda self: print("Action1"))
        self.A2.bind('<ButtonPress-1>', lambda self: print("Action2"))
        self.A3.bind('<ButtonPress-1>', lambda self: print("Action3"))
        self.A4.bind('<ButtonPress-1>', lambda self: print("Action4"))
        self.A5.bind('<ButtonPress-1>', lambda self: print("Action5"))
        self.A6.bind('<ButtonPress-1>', lambda self: print("Action6"))
        
        # Button Placement in 2x3 Grid    # Action Button effects
        self.A1.grid(column=0, row=0, sticky='news')
        self.A2.grid(column=1, row=0, sticky='news')
        self.A3.grid(column=2, row=0, sticky='news')
        self.A4.grid(column=0, row=1, sticky='news')
        self.A5.grid(column=1, row=1, sticky='news')
        self.A6.grid(column=2, row=1, sticky='news')

        # Buttons resize to fit frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
