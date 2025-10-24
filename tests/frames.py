import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("FOCUS")

testImg = tk.PhotoImage(file="./content/testFull.png")

# Side1 Frame
Side1 = tk.Frame(root, width=200, height=200, bg="skyblue")
Side1Label = tk.Label(Side1, text="Side1Label", bg="skyblue")
Side1Body = tk.Label(Side1, text="111")

# Side2 Frame
Side2 = tk.Frame(root, width=200, height=200, bg="skyblue")
Side2Label = tk.Label(Side2, text="Side2Label", bg="skyblue")
Side2Img = tk.Label(Side2, text="222")

# Big Image frame
BigImg = tk.Frame(root, width=600, height=600, bg="grey")
display_image = testImg.subsample(2, 2)
BigImgText = tk.Label(BigImg, text="Edited Image", bg="grey", fg="white")
BigImgCanv = tk.Canvas(BigImg)
BigImgCanv.create_image(0,0, image=display_image, anchor='nw')



# Grid placement
root.columnconfigure(0, weight=3)
root.rowconfigure(0, weight=3)
root.columnconfigure(3, weight=1)
root.rowconfigure(3, weight=1)

BigImg.grid(column=0, row=0, columnspan=3, rowspan=3, sticky='news')
BigImg.columnconfigure(0, weight=3)
BigImg.rowconfigure(0, weight=3)

BigImgText.grid(column=0, row=0)
BigImgCanv.grid(column=0, row=1)

Side1.grid(column=3, row=0, sticky='news')
Side1.columnconfigure(0, weight=1)
Side1.rowconfigure(0, weight=1)

Side1Label.grid(column=0, row=0)

Side1Body.grid(column=0, row=1, sticky='news')
Side1Body.columnconfigure(0, weight=1)
Side1Body.rowconfigure(0, weight=1)

Side2.grid(column=3, row=1)
Side2.columnconfigure(0, weight=1)
Side2.rowconfigure(0, weight=1)

Side2Label.grid(column=0, row=0)
Side2Img.grid(column=0, row=1)


root.mainloop()