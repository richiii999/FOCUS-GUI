# main.py

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

import Tools # Contains string manipulation stuff
import API # ./API.py: Contains API calls to webui


context = []
iterDelay = 5
modelNum = 1 # Which model from API.Models is being used?

def PromptAI(prompt) -> str:
    global context
    context.append({"role":"user", "content":Tools.sanitize(prompt)})
    response = API.chat_with_collection(API.Models[modelNum], context, API.KBIDs[1])

    response = response['choices'][0]['message']['content']
    context.append({"role":"assistant", "content":Tools.sanitize(response)})

    return response

def EndStudySession(): # Writes the response to summaryPrompt into the StudyHistory.txt file
    print('\nEnding study session...')

    print('Stopping sensors...')
    ffmpeg.terminate() # ffmpeg sometimes doesnt terminate, so just spam it 
    for s in sensors[1:]: s.terminate()
    for f in procs.values(): f.close() 

    with open('./KB/StudyHistory.txt', 'a') as f1, open('./LLM/SummaryPrompt.txt', 'r') as p: 
        print('Generating Summary...')
        f1.write('\n' + PromptAI(Tools.ReadFileAsLine(p))) # Prompt Summary, append it to history file
    with open('./KB/StudyHistory.txt', 'r') as f1, open('./KB/Knowledge.txt', 'w') as f2, open('./LLM/KnowledgePrompt.txt', 'r') as p:
        global context
        context = [] # reset the context

        f2.truncate(0) # Replace old knowledge with new knowledge
        print('Generating Knowledge...')
        f2.write(PromptAI(Tools.ReadFileAsLine(p) + Tools.ReadFileAsLine(f1)))

    print('Clearing old knowledge base files...')
    for i in API.KBIDs: API.delete_knowledge(i) # Delete knowledge bases
    subprocess.run("rm ./.open-webui/uploads/*", shell=True)
    subprocess.run("cd ./.open-webui/vector_db && rm -r `ls | grep -v 'chroma.sqlite3'`", shell=True)

    print("\nExiting...\n")

def Sense() -> str: # Gather output from the sensors
    sensorData = f"Time = {int(time.time() - startTime)} minutes, Aggregated Sensor data:\n"
    for f in procs.values(): # Get most recent output per sensor 
        f.seek(0)
        sensorData += f.readlines()[-1]
    return sensorData

def DistractionDetection(sensorData) -> str: # Prompt the AI WITHOUT CONTEXT for a 'yes' or 'no' response
    inp = "Based on the following sensor data, is the user in anyway not focused? 'yes' or 'no' only\n" + sensorData
    resp = API.chat_with_model(API.Models[modelNum], [{"role":"user", "content":Tools.sanitize(inp)}])['choices'][0]['message']['content'].lower().replace('.','')
    return resp


def StartChatting(response=""):
    """Starts a chat session by either listing available models or selecting one."""
    global modelNum
    if response == "": 
        API.Models += subprocess.check_output( # Fetch available models from the docker container
            "sudo docker exec -it 34e768ba1a4f ollama list | grep -v NAME | awk '{print $1}'", 
            shell=True).decode('utf-8').split('\n')[:-1] # List models, formatted
        return API.Models # Return the models list for the GUI to use
    
    else: modelNum = int(response) # Select model from the list

def Chatting(user_input: str) -> str:
    """Handles the main chat loop where the user interacts with the model."""
    # Get the AI response from PromptAI
    response = PromptAI(user_input)
    return response

def FormatActions(actionsList:str) -> dict: # Takes response from GenerateActions and tries to format it
    # The response should be something like "1. **Name**: desc."
    # This is bad since the ai response not deterministic, we basically just ask it nicely to format a certain way.
    
    formattedActions = {}

    for line in actionsList: 
        if not ("**" in line) or (":" in line and "." in line): 
            print(f"skipping {line}")
            continue # Skip non-list lines
        formattedActions[FindBetween(line, "**", "**")] = FindBetween(line, ":", "\n")

    return formattedActions

def GenerateActions(numActions:int, formatted:bool=False): 
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
    
