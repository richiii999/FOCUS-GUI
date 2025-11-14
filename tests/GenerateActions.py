import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import Tools
import API
import SLMResponse as SLM

SLM.StartChatting() # Initialize the models list

rawResponse = SLM.GenerateActions(3,False)
print("unformatted=\n"+rawResponse) # Prompt the AI for some actions

formattedResponse = Tools.FormatActions(rawResponse)
print(f"formatted=\n{formattedResponse}")

print("unpacked=")
for k,v in formattedResponse.items():
    print(f"{k} : {v}")