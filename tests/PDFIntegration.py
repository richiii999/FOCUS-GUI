import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk

from modules import RootWindow, BaseFrames, PDFViewer

# Add base frames
Base = BaseFrames.BaseFrames(RootWindow.root)

# Add the PDF viewer on the Left
PDFV = PDFViewer.PDFViewer(Base.L)


RootWindow.root.mainloop()
