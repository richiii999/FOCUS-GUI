import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import Tools
import API
import SLMResponse as SLM

SLM.StartChatting() # Initialize the models list

if input("Test1: Formatting the response (y/N)") == 'y':
    rawResponse = SLM.GenerateActions(3,False)
    print("unformatted=\n"+rawResponse) # Prompt the AI for some actions

    formattedResponse = Tools.FormatActions(rawResponse)
    print(f"formatted=\n{formattedResponse}")

    print("unpacked=")
    for k,v in formattedResponse.items():
        print(f"{k} : {v}")

if input("Test2: Verifying it came from the KB (y/N)") == 'y':
    with open('./Prompts/Para/GenerateActions.txt', 'r') as f1:
        prompt = Tools.ReadFileAsLine(f1)
        prompt = prompt.replace("NUMACTIONS", f"{3}")

        prompt += "At the end, please state cite why you chose these particular actions"

        TempContext = [{"role":"user", "content":prompt}]

    response = API.chat_with_collection(API.Models[modelNum], TempContext, API.KBIDs[0])['choices'][0]['message']['content']
    
    print(response)
    