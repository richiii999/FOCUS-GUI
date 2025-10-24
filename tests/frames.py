import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("FOCUS")

testImg = tk.PhotoImage(file="./content/testFull.png")

# Side1 Frame
Side1 = tk.Frame(root, width=200, height=200, bg="skyblue")
Side1Text = tk.Label(Side1, text="Side1", bg="skyblue")
thumbnail_image1 = testImg.subsample(6, 6)
Side1Img = tk.Label(Side1, image=thumbnail_image1)

# Side2 Frame
Side2 = tk.Frame(root, width=200, height=200, bg="skyblue")
Side2Text = tk.Label(Side2, text="Side2", bg="skyblue")
thumbnail_image2 = testImg.subsample(6, 6)
Side2Img = tk.Label(Side2, image=thumbnail_image2)

# Big Image frame
BigImg = tk.Frame(root, width=400, height=400, bg="grey")
display_image = testImg.subsample(2, 2)
BigImgText = tk.Label(BigImg, text="Edited Image", bg="grey", fg="white")
BigImgImg = tk.Label(BigImg, image=display_image)

# Grid placement
BigImg.grid(column=0, row=0, columnspan=3, rowspan=2)
BigImgText.grid(column=0, row=0)
BigImgImg.grid(column=0, row=1)

Side1.grid(column=3, row=0)
Side1Text.grid(column=0, row=0)
Side1Img.grid(column=0, row=1)

Side2.grid(column=3, row=1)
Side2Text.grid(column=0, row=0)
Side2Img.grid(column=0, row=1)


root.mainloop()