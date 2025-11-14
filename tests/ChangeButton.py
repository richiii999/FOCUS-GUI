import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)
import Tools

import tkinter as tk
from tkinter import ttk

from modules import RootWindow, BaseFrames, ActionButtons

# Add base frames
Base = BaseFrames.BaseFrames(RootWindow.root)

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

input("Test 3: SLM chat")
from modules import ChatWindow
Chat = ChatWindow.ChatWindow(Base.BR) # Add chat window

AB.UpdateButton(3, "SLM Hello", lambda e: Chat.send_message("Say Hello")) # AI should respond to this

input("Test 4: Pull from action list")
rawResponse = SLM.GenerateActions(3,False) # Generate 3 actions

formattedResponse = Tools.FormatActions(rawResponse) # Put them in a dict
print(f"Generated Actions:\n{rawResponse}")

from random import randrange

chosenNum = randrange(3) # Randomly pick one of 3 actions
label = list(formattedResponse)[chosenNum]
desc = list(formattedResponse.values())[chosenNum]

AB.UpdateButton(4, label, lambda e: Chat.send_message("Instruct the user to perform the following task: " + desc, False))


# Start
RootWindow.root.mainloop()
