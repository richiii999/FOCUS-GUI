import sys
sys.path.append(".")  # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
import SLMResponse
from tkinter import ttk

import Tools

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

# PDF Viewer on Left, Buttons -> TopRight, Chat BottomRight
PDFV = PDFViewer.PDFViewer(Base.L)
AB = ActionButtons.ActionButtons(Base.TR, 6)
Chat = ChatWindow.ChatWindow(Base.BR, PDFV) # Connects to PDFV to access the pageNum

# Action button bindings
AB.buttons[0].config(text="Quiz")
AB.buttons[0].bind('<ButtonPress-1>', lambda e: QuizModule.QuizWindow(Chat, SLMResponse.Chatting(Tools.ReadFileAsLine("./Prompts/QuizPrompt.txt"))))
AB.buttons[1].config(text="Break")
AB.buttons[1].bind('<ButtonPress-1>', lambda e: Chat.start_break())
AB.buttons[2].config(text="Summary")
AB.buttons[2].bind('<ButtonPress-1>', lambda e: Chat.send_message(Tools.ReadFileAsLine("./Prompts/SummaryAction.txt"), False))

root.mainloop()