import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk

from modules import PDFViewer

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

# Action Buttons
A1 = tk.Button(Side1, text="A1", bg="red",    relief='ridge', borderwidth=3)
A2 = tk.Button(Side1, text="A2", bg="green",  relief='ridge', borderwidth=3)
A3 = tk.Button(Side1, text="A3", bg="blue",   relief='ridge', borderwidth=3)
A4 = tk.Button(Side1, text="A4", bg="yellow", relief='ridge', borderwidth=3)
A5 = tk.Button(Side1, text="A5", bg="purple", relief='ridge', borderwidth=3)
A6 = tk.Button(Side1, text="A6", bg="cyan",   relief='ridge', borderwidth=3)

# Action Button effects
def Action1(s): print(f"Action1: {s}")
def Action2(s): print(f"Action2: {s}")
def Action3(s): print(f"Action3: {s}")
def Action4(s): print(f"Action4: {s}")
def Action5(s): print(f"Action5: {s}")
def Action6(s): print(f"Action6: {s}")

A1.bind('<ButtonPress-1>', lambda e: Action1("test1"))
A2.bind('<ButtonPress-1>', lambda e: Action2("test2"))
A3.bind('<ButtonPress-1>', lambda e: Action3("test3"))
A4.bind('<ButtonPress-1>', lambda e: Action4("test4"))
A5.bind('<ButtonPress-1>', lambda e: Action5("test5"))
A6.bind('<ButtonPress-1>', lambda e: Action6("test6"))



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

pdf_viewer = PDFViewer.PDFViewer(BigImg)
pdf_viewer.grid(column=0, row=0, sticky='news')

# Side1
Side1.grid(column=1, row=0, sticky='news')
Side1.columnconfigure(0, weight=1)
Side1.columnconfigure(1, weight=1)
Side1.columnconfigure(2, weight=1)
Side1.rowconfigure(0, weight=1)
Side1.rowconfigure(1, weight=1)

# Side2
Side2.grid(column=1, row=1, sticky='news')
Side2.columnconfigure(0, weight=1)
Side2.rowconfigure(0, weight=1)

Side2Label.grid(column=0, row=0, sticky='news')

## Action buttons
A1.grid(column=0, row=0, sticky='news')
A2.grid(column=1, row=0, sticky='news')
A3.grid(column=2, row=0, sticky='news')
A4.grid(column=0, row=1, sticky='news')
A5.grid(column=1, row=1, sticky='news')
A6.grid(column=2, row=1, sticky='news')



root.mainloop()
