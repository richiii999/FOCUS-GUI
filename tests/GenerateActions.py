import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import API
import SLMResponse as SLM

SLM.StartChatting() # Initialize the models list
print(SLM.GenerateActions(5)) # Prompt the AI for some actions
