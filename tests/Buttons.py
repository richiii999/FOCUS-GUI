import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk

from modules import ActionButtons

## Root window
root = tk.Tk()
root.title("FOCUS")
root.geometry('800x600')

## Making the frames
# Side1 Frame (top right)
Side1 = tk.Frame(root, width=400, height=400, bg="skyblue", relief='ridge', borderwidth=5)
Side1Label = tk.Label(Side1, text="Side1Label", bg="skyblue")

# Side2 Frame (Bottom right)
Side2 = tk.Frame(root, width=400, height=400, bg="skyblue", relief='ridge', borderwidth=5)
Side2Label = tk.Label(Side2, text="Side2Label", bg="skyblue")

# Big Image frame (left)
BigImg = tk.Frame(root, width=800, height=800, bg="grey", relief='ridge', borderwidth=5)




## Grid placement
# Root Grid
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)

# BigImg
BigImg.grid(column=0, row=0, columnspan=1, rowspan=2, sticky='news')
BigImg.columnconfigure(0, weight=2)
BigImg.rowconfigure(0, weight=2)

# Side1
Side1.grid(column=1, row=0, sticky='news')
Side1.columnconfigure(0, weight=1)
Side1.rowconfigure(0, weight=1)

# Action Buttons
AB = ActionButtons.ActionButtons(Side1, 6)

# Side2
Side2.grid(column=1, row=1, sticky='news')
Side2.columnconfigure(0, weight=1)
Side2.rowconfigure(0, weight=1)

Side2Label.grid(column=0, row=0, sticky='news')

root.mainloop()
