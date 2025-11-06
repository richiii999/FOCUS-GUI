import tkinter as tk
from tkinter import ttk

class ActionButtons(tk.Frame):
    # Action Button effects
    def Action1(self, s="test1"): print(f"Action1: {s}")
    def Action2(self, s="test2"): print(f"Action2: {s}")
    def Action3(self, s="test3"): print(f"Action3: {s}")
    def Action4(self, s="test4"): print(f"Action4: {s}")
    def Action5(self, s="test5"): print(f"Action5: {s}")
    def Action6(self, s="test6"): print(f"Action6: {s}")

    def __init__(self, master):
        # Action Buttons
        super().__init__(master)
        self.A1 = tk.Button(self, text="A1", command=self.Action1, bg="red",    relief='ridge', borderwidth=3)
        self.A2 = tk.Button(self, text="A2", command=self.Action2, bg="green",  relief='ridge', borderwidth=3)
        self.A3 = tk.Button(self, text="A3", command=self.Action3, bg="blue",   relief='ridge', borderwidth=3)
        self.A4 = tk.Button(self, text="A4", command=self.Action4, bg="yellow", relief='ridge', borderwidth=3)
        self.A5 = tk.Button(self, text="A5", command=self.Action5, bg="purple", relief='ridge', borderwidth=3)
        self.A6 = tk.Button(self, text="A6", command=self.Action6, bg="cyan",   relief='ridge', borderwidth=3)

        # Button Placement in 2x3 Grid
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

    