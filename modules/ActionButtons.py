import tkinter as tk

def clone(widget, newParent): # Can't reparent: https://stackoverflow.com/questions/46505982/is-there-a-way-to-clone-a-tkinter-widget 
    clone = widget.__class__(newParent)
    for key in widget.configure(): clone.configure({key: widget.cget(key)})
    return clone

class ActionButtons(tk.Frame):
    def __init__(self, master, buttonsCount=9, perRow=3):
        super().__init__(master)

        self.buttons = []

        for i in range(buttonsCount): # Create each button
            currRow = int(i/perRow)
            currCol = i%perRow
            print(f" creating button_{i} @ {currRow},{currCol}")

            self.buttons.append(tk.Button(self, text=f"Button_{str(i)}", bg="red", relief='ridge', borderwidth=3))
            
            self.buttons[i].grid(column=currCol, row=currRow, sticky='news') # Button Placement in Grid
            self.columnconfigure(currCol, weight=1) # Grid resize to fit new button
            self.rowconfigure(currRow, weight=1)
        
        numInLastRow = buttonsCount % perRow  # Last row of buttons resized to fill empty space 
        lastRowPos = int(buttonsCount/perRow) # ex. [1][2][_][_] -> [ 1 ][ 2 ]

        if (numInLastRow): # Create frame specifically for the last row
            lastRow = tk.Frame(self) 
            lastRow.grid(column=0, row=lastRowPos, columnspan=perRow, sticky='news')
            lastRow.rowconfigure(0, weight=1)

            for i in range(buttonsCount - (numInLastRow), buttonsCount): 
                print(f" resizing button_{i}")
                self.buttons[i].grid_forget() # unGrid the last row of buttons
                self.buttons[i] = clone(self.buttons[i], lastRow)  
                
                lastRow.columnconfigure(i, weight=1) # Grid new buttons
                self.buttons[i].grid(row=0, column=i, sticky='news')
            
        # Default bindings, must be done after replacing the last row. Clone() doesnt preserve bindings I guess
        for i in range(buttonsCount): self.buttons[i].bind('<ButtonPress-1>', self.defaultAction) 
        
        self.grid(column=0, row=0, sticky='news') # Auto Self-placement within parent frame
    
    def defaultAction(self, buttonEvent): # Default button action: Disable the button on click
        print(f"Button pressed: {buttonEvent.widget}")
        buttonEvent.widget.config(state=tk.DISABLED)

    def UpdateButton(self, buttonNum:int=-1, newLabel:str="", newFunc=None):
        if buttonNum not in range (len(self.buttons)): 
            print(f"ButtonNum {buttonNum} not in buttons[] range(0-{len(self.buttons)})")
            return
        
        b = self.buttons[buttonNum]
        b.configure(text=newLabel)
        if newFunc: b.bind('<ButtonPress-1>', newFunc)

        print(f"Updated Button {buttonNum}, {newLabel}, to bind to {newFunc}")