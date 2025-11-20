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
Chat = ChatWindow.ChatWindow(Base.BR)

parentName = Chat.winfo_parent()
parent     = Chat._nametowidget(parentName)
siblings = parent.winfo_children()

print(siblings)