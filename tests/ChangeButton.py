import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)
import Tools

import tkinter as tk
from tkinter import ttk

from modules import BaseFrames, ActionButtons

# Setup Root window
root = tk.Tk()
root.title("FOCUS")
root.geometry('800x600')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add base frames
Base = BaseFrames.BaseFrames(root)

# Add Buttons in the top right
numButtons = 8
print(f"There should be {numButtons} Buttons")
AB = ActionButtons.ActionButtons(Base.TR, numButtons)

### ^^^ Copied from previous test: Buttons.py
input("Run tests?")

import SLMResponse as SLM

input("Test 1: Valid Button Change")
AB.UpdateButton(0, "UpdatedButton", lambda e: print("Updated Button Test")) # Should change the first button

input("Test 2: Invalid Button Change (idx of button outside range)")
AB.UpdateButton(99, "FailedButton") # Shouldnt change, should print the error

# input("Test 3: SLM chat")
# from modules import ChatWindow
# Chat = ChatWindow.ChatWindow(Base.BR) # Add chat window

# AB.UpdateButton(3, "SLM Chat", lambda e: Chat.send_message("Say Hello")) # AI should respond to this

input("Test 4: Pull from action list")
# rawResponse = SLM.GenerateActions(3,False) # Generate 3 actions
rawResponse = """testline
1. **Task1**: Say 'Task1'.
2. **Task2**: Say 'Task2'.
3. **Task3**: Say 'Task3'.
testtest"""

formattedResponse = Tools.FormatActions(rawResponse) # Put them in a dict
print(f"Generated Actions:\n{rawResponse}")

from random import randrange
randomAction = list(formattedResponse)[randrange(3)] # Randomly pick one of 3 actions



AB.UpdateButton(4, randomAction)


root.mainloop()
