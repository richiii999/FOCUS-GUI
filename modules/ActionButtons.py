import tkinter as tk

# TODO fix BUG where default buttons bindings are only on last button, not themselves

def clone(widget, newParent): # Can't reparent: https://stackoverflow.com/questions/46505982/is-there-a-way-to-clone-a-tkinter-widget 
    cls = widget.__class__
    clone = cls(newParent)
    for key in widget.configure(): clone.configure({key: widget.cget(key)})
    
    return clone

class ActionButtons(tk.Frame):
    def __init__(self, master, buttonsCount=9, perRow=3):
        super().__init__(master) # Required idk

        self.buttons = []

        for i in range(buttonsCount): # Create each button
            currRow = int(i/perRow)
            currCol = i%perRow
            print(f" creating button_{i} @ {currRow},{currCol}")

            self.buttons.append(tk.Button(self, text=f"Button_{str(i)}", bg="red", relief='ridge', borderwidth=3))
            self.buttons[i].bind('<ButtonPress-1>', lambda e: self.buttons[i].config(state=tk.DISABLED)) # Action Button default bindings
            self.buttons[i].grid(column=currCol, row=currRow, sticky='news') # Button Placement in Grid
            
            self.columnconfigure(currCol, weight=1) # Grid resize to fit new button
            self.rowconfigure(currRow, weight=1)
        
        # Last row of buttons resized to fill empty space ex. [1][2][_][_] -> [ 1 ][ 2 ]
        numInLastRow = buttonsCount % perRow
        lastRowPos = int(buttonsCount/perRow)

        if (numInLastRow):
            # print(f"{numInLastRow} in last row (row {lastRowPos}) need resizing")

            lastRow = tk.Frame(self)
            lastRow.grid(column=0, row=lastRowPos, columnspan=perRow, sticky='news')
            lastRow.rowconfigure(0, weight=1)
            for i in range(numInLastRow): lastRow.columnconfigure(i, weight=1)

            col = 0
            for i in range(buttonsCount - (numInLastRow), buttonsCount): 
                print(f" resizing button_{i}")
                self.buttons[i].grid_forget() # unGrid the last row of buttons
                self.buttons[i] = clone(self.buttons[i], lastRow)  
                self.buttons[i].grid(row=0, column=col, sticky='news')
                col += 1

        self.grid(column=0, row=0, sticky='news') # Auto Self-placement
