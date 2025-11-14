import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import API
import SLMResponse as SLM

SLM.StartChatting() # Initialize the models list

rawResponse = SLM.GenerateActions(3,False)
print("unformatted=\n"+rawResponse) # Prompt the AI for some actions

print("formatted=")

formattedResponse = SLM.GenerateActions(3,True)
for k,v in formattedResponse:
    print(f"{k} : {v}")


print(f"dict={formattedResponse}")