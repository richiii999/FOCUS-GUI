import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("1600x900")
root.title("FOCUS")

testImg = tk.PhotoImage(file="./content/test200x200.png")

# Grid Layout: 2x2
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)

# Grid cell test (works)
TL = ttk.Label(root, image=testImg)
TR = ttk.Label(root, image=testImg)
BL = ttk.Label(root, image=testImg)
BR = ttk.Label(root, image=testImg)
TL.grid(column=0, row=0)
TR.grid(column=0, row=1)
BL.grid(column=1, row=0)
BR.grid(column=1, row=1)

# old frames
# # Orig Image Grid
# tools_frame = tk.Frame(root, width=200, height=400, bg="skyblue")
# tools_frame.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.Y)
# tk.Label(
#     tools_frame,
#     text="Original Image",
#     bg="skyblue",
# ).pack(padx=5, pady=5)
# thumbnail_image = image.subsample(5, 5)
# tk.Label(tools_frame, image=thumbnail_image).pack(padx=5, pady=5)

# # Tools frame
# tools_tab = tk.Frame(root, bg="lightblue")
# tools_tab.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.Y)
# tools_var = tk.StringVar(value="None")
# for tool in ["Resizing", "Rotating"]:
#     tk.Radiobutton(
#         tools_tab,
#         text=tool,
#         variable=tools_var,
#         value=tool,
#         bg="lightblue",
#     ).pack(anchor="w", padx=20, pady=5)

# # Image frame
# image_frame = tk.Frame(root, width=400, height=400, bg="grey")
# image_frame.pack(padx=5, pady=5, side=tk.LEFT)
# display_image = image.subsample(2, 2)
# tk.Label(
#     image_frame,
#     text="Edited Image",
#     bg="grey",
#     fg="white",
# ).pack(padx=5, pady=5)
# tk.Label(image_frame, image=display_image).pack(padx=5, pady=5)

root.mainloop()