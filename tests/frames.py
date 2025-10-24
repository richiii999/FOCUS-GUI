from tkinter import *
from tkinter import ttk

root = Tk()

l =ttk.Label(root, width=30, padding=5, text="Starting...", )

def changeText(s): l.configure(text=s) # Change the text 

l.grid()

l.bind('<Enter>', lambda e: l.configure(text='Moved mouse inside'))
l.bind('<Leave>', lambda e: l.configure(text='Moved mouse outside'))
l.bind('<ButtonPress-1>', lambda e: l.configure(text='Clicked left mouse button'))
l.bind('<3>', lambda e: l.configure(text='Clicked third mouse button'))
l.bind('<Double-1>', lambda e: l.configure(text='Double clicked'))
l.bind('<B3-Motion>', lambda e: l.configure(text=f'third button drag to {e.x},{e.y}'))

root.mainloop()