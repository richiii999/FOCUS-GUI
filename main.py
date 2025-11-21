# Main.py

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

import API # Contains API calls to webui
from modules import Sensors # Controls the face+gaze trackers

def EndStudySession(): # Writes the response to summaryPrompt into the StudyHistory.txt file
    print('\nEnding study session...')

    Sensors.StopSensors()

    # with open('./KB/StudyHistory.txt', 'a') as f1, open('./LLM/SummaryPrompt.txt', 'r') as p: 
    #     print('Generating Summary...')
    #     f1.write('\n' + PromptAI(Tools.ReadFileAsLine(p))) # Prompt Summary, append it to history file
    # with open('./KB/StudyHistory.txt', 'r') as f1, open('./KB/Knowledge.txt', 'w') as f2, open('./LLM/KnowledgePrompt.txt', 'r') as p:
    #     global context
    #     context = [] # reset the context

    #     f2.truncate(0) # Replace old knowledge with new knowledge
    #     print('Generating Knowledge...')
    #     f2.write(PromptAI(Tools.ReadFileAsLine(p) + Tools.ReadFileAsLine(f1)))

    # print('Clearing old knowledge base files...')
    # for i in API.KBIDs: API.delete_knowledge(i) # Delete knowledge bases
    # subprocess.run("rm ./.open-webui/uploads/*", shell=True)
    # subprocess.run("cd ./.open-webui/vector_db && rm -r `ls | grep -v 'chroma.sqlite3'`", shell=True)

    print("\nExiting FOCUS...\n")



# Hmm might need to multithread this or something, 
# sensors has a inf while loop but so does GUI
try:
    Sensors.StartSensors()
    while True: 
        print(Sensors.Sense())
        time.sleep(Sensors.iterDelay)

except KeyboardInterrupt: Sensors.StopSensors()



import GUI # Start the GUI