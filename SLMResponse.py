# main.py

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

import API # ./API.py: Contains API calls to webui
context = []
iterDelay = 5

def PromptAI(prompt) -> str:
    global context
    context.append({"role":"user", "content":sanitize(prompt)})
    response = API.chat_with_collection(API.Models[modelNum], context, API.KBIDs[1])

    response = response['choices'][0]['message']['content']
    context.append({"role":"assistant", "content":sanitize(response)})

    return response

def EndStudySession(): # Writes the response to summaryPrompt into the StudyHistory.txt file
    print('\nEnding study session...')

    print('Stopping sensors...')
    ffmpeg.terminate() # ffmpeg sometimes doesnt terminate, so just spam it 
    for s in sensors[1:]: s.terminate()
    for f in procs.values(): f.close() 

    with open('./KB/StudyHistory.txt', 'a') as f1, open('./LLM/SummaryPrompt.txt', 'r') as p: 
        print('Generating Summary...')
        f1.write('\n' + PromptAI(ReadFileAsLine(p))) # Prompt Summary, append it to history file
    with open('./KB/StudyHistory.txt', 'r') as f1, open('./KB/Knowledge.txt', 'w') as f2, open('./LLM/KnowledgePrompt.txt', 'r') as p:
        global context
        context = [] # reset the context

        f2.truncate(0) # Replace old knowledge with new knowledge
        print('Generating Knowledge...')
        f2.write(PromptAI(ReadFileAsLine(p) + ReadFileAsLine(f1)))

    print('Clearing old knowledge base files...')
    for i in API.KBIDs: API.delete_knowledge(i) # Delete knowledge bases
    subprocess.run("rm ./.open-webui/uploads/*", shell=True)
    subprocess.run("cd ./.open-webui/vector_db && rm -r `ls | grep -v 'chroma.sqlite3'`", shell=True)

    print("\nExiting...\n")

def ReadFileAsLine(f) -> str:
    s = ''
    for line in f.readlines(): s += sanitize(line).replace('\n',' ')
    return s

def sanitize(s) -> str: # Remove characters that cause issues from a str
    s = s.replace("\'", "")
    s = s.replace("\"", "")
    return s

def UserInput(inputPrompt, validinput=None) -> str: # User input verification
    i = input(inputPrompt)
    while i not in validinput: i = input("Invalid input, try again\n" + inputPrompt)
    return i

def Sense() -> str: # Gather output from the sensors
    sensorData = f"Time = {int(time.time() - startTime)} minutes, Aggregated Sensor data:\n"
    for f in procs.values(): # Get most recent output per sensor 
        f.seek(0)
        sensorData += f.readlines()[-1]
    return sensorData

def DistractionDetection(sensorData) -> str: # Prompt the AI WITHOUT CONTEXT for a 'yes' or 'no' response
    inp = "Based on the following sensor data, is the user in anyway not focused? 'yes' or 'no' only\n" + sensorData
    resp = API.chat_with_model(API.Models[modelNum], [{"role":"user", "content":sanitize(inp)}])['choices'][0]['message']['content'].lower().replace('.','')
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

def sanitize(s: str) -> str:
    """Sanitize the input string by removing problematic characters."""
    s = s.replace("\'", "")
    s = s.replace("\"", "")
    return s

def Chatting(user_input: str) -> str:
    """Handles the main chat loop where the user interacts with the model."""
    # Get the AI response from PromptAI
    response = PromptAI(user_input)
    return response

def ActionsListPrompt(numActions:int) -> str: # Prompts the AI to generate a list of N actions, returns response 
    print("Getting action space via RAG...")
    with open('./Prompts/GenerateActions.txt', 'r') as f1:
        TempContext = [{"role":"user", "content":ReadFileAsLine(f1)}]
        return API.chat_with_collection(API.Models[modelNum], TempContext, API.KBIDs[0])['choices'][0]['message']['content']

