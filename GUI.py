# GUI.py 
# Uses our tkinter modules that create & assemble the frames 

import tkinter as tk
import SLMResponse
from tkinter import ttk

import Tools

from modules import RootWindow, BaseFrames, ActionButtons, ChatWindow, PDFViewer, QuizModule

# Add base frames
Base = BaseFrames.BaseFrames(RootWindow.root)

# PDF Viewer on Left, Buttons -> TopRight, Chat BottomRight
PDFV = PDFViewer.PDFViewer(Base.L)
AB = ActionButtons.ActionButtons(Base.TR, 6)
Chat = ChatWindow.ChatWindow(Base.BR, PDFV) # Connects to PDFV to access the pageNum

# Action button bindings
AB.buttons[0].config(text="Quiz")
AB.buttons[0].bind('<ButtonPress-1>', lambda e: QuizModule.QuizWindow(Chat, SLMResponse.PromptAI(Tools.ReadFileAsLine("./Prompts/QuizPrompt.txt"))))
AB.buttons[1].config(text="Break")
AB.buttons[1].bind('<ButtonPress-1>', lambda e: Chat.start_break())
AB.buttons[2].config(text="Summary")
AB.buttons[2].bind('<ButtonPress-1>', lambda e: Chat.send_message(Tools.ReadFileAsLine("./Prompts/SummaryAction.txt"), False))

# Dynamic Action button
rawResponse = SLMResponse.GenerateActions(3,False) # Generate 3 actions

formattedResponse = Tools.FormatActions(rawResponse) # Put them in a dict
print(f"Generated Actions:\n{rawResponse}")

from random import randrange

for i in range(3): # Use all 3 actions in the buttons
    label = list(formattedResponse)[i]
    desc = list(formattedResponse.values())[i]
    AB.UpdateButton(3+i, label, lambda e: Chat.send_message("Instruct the user to perform the following task: " + desc, False))
    # print(f"{i} = {label} {desc}")


RootWindow.root.mainloop()