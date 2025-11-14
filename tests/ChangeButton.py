import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

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

input("Test 3: SLM chat")
AB.UpdateButton(1, "SLM Chat", lambda e: SLM.PromptAI("Say 'Hello'"))

input("Test 4: Pull from action list")




root.mainloop()
