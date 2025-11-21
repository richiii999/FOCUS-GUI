# SLMResponse.py
# Contains funcs to prompt the AI and interact with the API & Sensors

import sys
import time
from subprocess import check_output # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

import Tools # Contains string manipulation stuff
import API # Contains API calls to webui

context = []
iterDelay = 5
modelNum = 1 # Which model from API.Models is being used?

PDFV = None # Optional reference to the pdf viewer (so we can get the curr pageNum)
sensorFiles = [ # references to sensor log files
    "./SensorLogs/faceTracker.txt",
    "./SensorLogs/gazeTracker.txt"
] 

def PromptAI(prompt) -> str:
    global context
    context.append({"role":"user", "content":Tools.sanitize(prompt)})
    response = API.chat_with_collection(API.Models[modelNum], context, API.KBIDs[1])

    response = response['choices'][0]['message']['content'] 
    context.append({"role":"assistant", "content":Tools.sanitize(response)})

    return response

def DistractionDetection(sensorData) -> str: # Prompt the AI WITHOUT CONTEXT for a 'yes' or 'no' response
    prompt = "Based on the following sensor data, is the user in anyway not focused? 'yes' or 'no' only\n" + sensorData
    resp = API.chat_with_model(API.Models[modelNum], [{"role":"user", "content":Tools.sanitize(prompt)}])['choices'][0]['message']['content'].lower().replace('.','')
    return resp

def StartChatting(selectModel=-1):
    """Starts a chat session by either listing available models or selecting one."""
    global modelNum
    if selectModel == -1: 
        API.Models += check_output( # Fetch available models from the docker container
            "sudo docker exec -it 34e768ba1a4f ollama list | grep -v NAME | awk '{print $1}'", 
            shell=True).decode('utf-8').split('\n')[:-1] # List models, formatted
        return API.Models # Return the models list for the GUI to use
    
    else: modelNum = int(selectModel) # Select the given model from the list

def GenerateActions(numActions:int=3, formatted:bool=False): 
    """Prompts the AI to generate a list of N actions
    if formatted, returns the label and desc in a dict. 
    otherwise returns the raw response as a str"""
    
    print("Getting action space via RAG...")
    with open('./Prompts/Para/GenerateActions.txt', 'r') as f1:
        prompt = Tools.ReadFileAsLine(f1)
        prompt = prompt.replace("NUMACTIONS", f"{numActions}")

        TempContext = [{"role":"user", "content":prompt}]

    response = API.chat_with_collection(API.Models[modelNum], TempContext, API.KBIDs[0])['choices'][0]['message']['content']
    
    return FormatActions(response) if formatted else response

def PrependPrompt(prompt) -> str: # Prepend information to the given prompt
        prepend = "--- Prepended information for AI ---\n"
        
        if PDFV: prepend += f"Current page is: {PDFV.page_num}\n"
        for path in sensorFiles: prepend += f"{Tools.readLastLine(path)}\n" 

        prepend += "--- END prepended information for AI ---\n"
        return prepend + prompt

