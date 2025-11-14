import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk

from modules import RootWindow, BaseFrames, ActionButtons

# Add base frames
Base = BaseFrames.BaseFrames(RootWindow.root)

# Add Buttons in the top right
numButtons = 8
print(f"There should be {numButtons} Buttons")
AB = ActionButtons.ActionButtons(Base.TR, numButtons)


RootWindow.root.mainloop()
