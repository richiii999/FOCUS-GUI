import sys
sys.path.append(".")  # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk

from modules import BaseFrames, ActionButtons, ChatWindow

# Setup Root window
root = tk.Tk()
root.title("FOCUS")
root.geometry('800x600')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add Base Frames & Buttons
Base = BaseFrames.BaseFrames(root)
AB = ActionButtons.ActionButtons(Base.TR, 6)

# Add Chat Window in bottom-right frame
Chat = ChatWindow.ChatWindow(Base.BR)

# Action button bindings
AB.buttons[0].config(text="Quiz")
AB.buttons[0].bind('<ButtonPress-1>', lambda e: Chat.send_message("Generate a 5 question quiz of algebra", False))

root.mainloop()
