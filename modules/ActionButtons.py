import tkinter as tk
from tkinter import ttk

class ActionButtons(tk.Frame):
    def __init__(self, master, numButtons=9):
        super().__init__(master) # Required idk

        self.numButtons = numButtons # How many buttons in grid?

        # Action Buttons
        self.buttons = []

        for i in range(numButtons): 
            self.buttons.append(tk.Button(self, text=f"Button_{str(i)}", bg="red", relief='ridge', borderwidth=3))
            # Action Button default bindings
            self.buttons[i].bind('<ButtonPress-1>', lambda e: self.buttons[i].config(state=tk.DISABLED))
            # Button Placement in 2x3 Grid
            self.buttons[i].grid(column=i%3, row=int(i/3), sticky='news')
            
            # Buttons resize to fit 2x3 Grid
            self.columnconfigure(i%3, weight=1) # 3 cols
            self.rowconfigure(int(i/3), weight=1) # 3 buttons per row (dyn add rows as needed)
        
        self.grid(column=0, row=0, sticky='news') # Auto Self-placement
        