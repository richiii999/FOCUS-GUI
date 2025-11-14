import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import API
import SLMResponse as SLM

SLM.StartChatting() # Initialize the models list
print("unformatted=\n"+SLM.GenerateActions(3,False)) # Prompt the AI for some actions

print("formatted=")
for k,v in SLM.GenerateActions(3,True):
    print(f"{k} : {v}")