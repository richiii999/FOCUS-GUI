import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("FOCUS")

## Making the frames
# Side1 Frame
Side1 = tk.Frame(root, width=200, height=200, bg="skyblue", relief='ridge', borderwidth=5)
Side1Label = tk.Label(Side1, text="Side1Label", bg="skyblue")
Side1Body = tk.Label(Side1, text="Side1Body")

# Side2 Frame
Side2 = tk.Frame(root, width=200, height=200, bg="skyblue", relief='ridge', borderwidth=5)
Side2Label = tk.Label(Side2, text="Side2Label", bg="skyblue")
Side2Body = tk.Label(Side2, text="Side2Body")

# Big Image frame
BigImg = tk.Frame(root, width=400, height=400, bg="grey", relief='ridge', borderwidth=5)
BigImgLabel = tk.Label(BigImg, text="BigImgLabel", bg="grey")

## Grid placement
# Root
root.columnconfigure(0, weight=2)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# BigImg
BigImg.grid(column=0, row=0, columnspan=1, rowspan=2, sticky='news')
BigImg.columnconfigure(0, weight=2)
BigImg.rowconfigure(0, weight=2)
BigImgLabel.grid(column=0, row=0)

# Side1
Side1.grid(column=1, row=0, sticky='news')
Side1.columnconfigure(0, weight=1)
Side1.rowconfigure(0, weight=1)

Side1Label.grid(column=0, row=0)
Side1Body.grid(column=0, row=1)
Side1Body.columnconfigure(0, weight=1)
Side1Body.rowconfigure(0, weight=1)

# Side2
Side2.grid(column=1, row=1, sticky='news')
Side2.columnconfigure(0, weight=1)
Side2.rowconfigure(0, weight=1)

Side2Label.grid(column=0, row=0)
Side2Body.grid(column=0, row=1)
Side2Body.columnconfigure(0, weight=1)
Side2Body.rowconfigure(0, weight=1)


root.mainloop()