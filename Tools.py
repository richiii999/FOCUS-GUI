# String Manipulation and other useful funcs

def ReadFileAsLine(f) -> str:
    s = ''
    for line in f.readlines(): s += sanitize(line).replace('\n',' ')
    return s

def sanitize(s: str) -> str:
    """Sanitize the input string by removing problematic characters."""
    s = s.replace("\'", "")
    s = s.replace("\"", "")
    return s

def UserInput(inputPrompt, validinput=None) -> str: 
    """Input() but it must be within validInput"""
    i = input(inputPrompt)
    while i not in validinput: i = input("Invalid input, try again\n" + inputPrompt)
    return i

def FindBetween(s:str, start:str, end:str) -> str: 
    """Finds s between start:end, returns empty str if something wrong"""
    return s.split(start)[1].split(end)[0]
