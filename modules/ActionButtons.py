import tkinter as tk
from tkinter import ttk


# TODO fix BUG where buttons bindings are only on last button, not themselves

class ActionButtons(tk.Frame):
    def __init__(self, master, numButtons=9):
        super().__init__(master) # Required idk

        self.numButtons = numButtons # How many buttons in grid?
        self.buttons = [] # Action Buttons

        for i in range(numButtons): # Create each button
            self.buttons.append(tk.Button(self, text=f"Button_{str(i)}", bg="red", relief='ridge', borderwidth=3))
            self.buttons[i].bind('<ButtonPress-1>', lambda e: self.buttons[i].config(state=tk.DISABLED)) # Action Button default bindings
            self.buttons[i].grid(column=i%3, row=int(i/3), sticky='news') # Button Placement in 2x3 Grid
            
            # Buttons resize to fit a Grid
            self.columnconfigure(i%3, weight=1) # 3 cols
            self.rowconfigure(int(i/3), weight=1) # 3 buttons per row (more rows as needed)
        
        self.grid(column=0, row=0, sticky='news') # Auto Self-placement
        