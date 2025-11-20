import sys
sys.path.append(".")  # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk

from modules import BaseFrames, ActionButtons, ChatWindow, PDFViewer, QuizModule

# Setup Root window
root = tk.Tk()
root.title("FOCUS")
root.geometry('800x600')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add base frames
Base = BaseFrames.BaseFrames(root)

# Add the PDF viewer on the Left
PDFV = PDFViewer.PDFViewer(Base.L)

# Add Base Frames & Buttons
# Base = BaseFrames.BaseFrames(root)
AB = ActionButtons.ActionButtons(Base.TR, 6)

# Add Chat Window in bottom-right frame
Chat = ChatWindow.ChatWindow(Base.BR, PDFV)

# Action button bindings
AB.buttons[0].config(text="Quiz")
AB.buttons[0].bind('<ButtonPress-1>', lambda e: QuizModule.QuizWindow(Chat, Chat.send_message("Generate a 5 question quiz about algebra")))

AB.buttons[1].config(text="Break")
AB.buttons[1].bind('<ButtonPress-1>', lambda e: Chat.start_break())

# Summary
AB.buttons[2].config(text="Summary")
AB.buttons[2].bind('<ButtonPress-1>', lambda e: Chat.send_message("Give me a Summary of the previous slides", False))

root.mainloop()