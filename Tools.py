# String Manipulation and other useful funcs

def ReadFileAsLine(f) -> str:
    if isinstance(f, str): 
        with open("./Prompts/QuizPrompt.txt", 'r') as f1:
            s = ''
            for line in f1.readlines(): s += sanitize(line).replace('\n',' ')
            return s
    else:
        s = ''
        for line in f1.readlines(): s += sanitize(line).replace('\n',' ')
        return s

def sanitize(s: str) -> str:
    """Sanitize the input string by removing problematic characters."""
    s = s.replace("\'", "")
    s = s.replace("\"", "")
    return s

def UserInput(inputPrompt, validInput=None, defaultIdx=0) -> str: 
    """Input() but it must be within validInput (not case sensitive)"""
    i = input(inputPrompt).lower()
    if i == "" and validInput and defaultIdx > -1 and defaultIdx in range(len(validInput)): i = validInput[defaultIdx]
    while i not in validInput: i = input("Invalid input, try again\n" + inputPrompt).lower()
    return i

# From: https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
def FindBetween(s:str, start:str, end:str) -> str: 
    """Finds s between start:end, returns empty str if something wrong"""
    return s[s.find(start)+len(start):s.rfind(end)]

def FormatActions(actionsList:str) -> dict: # Takes response from SLM.GenerateActions() and tries to format it
    # The raw response (input) should be something like "1. **Name**: desc."
    # The formatted response (output) should be {"Name" : "desc"}
    # This is bad since the ai response not deterministic, we basically just ask it nicely to format a certain way.
    
    formattedActions = {}

    for line in actionsList.split('\n'): 
        if not ("**" in line) or not (":" in line and "." in line): 
            print(f"skipping {line}")
            continue # Skip non-list lines
        formattedActions[FindBetween(line, "**", "**")] = FindBetween(line, ":", ".")

    return formattedActions