# Main.py

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)
import threading # Multithread the sensors and GUI separately

import API # Contains API calls to webui
from modules import Sensors # Controls the face+gaze trackers
import SLMResponse # Model controls
import Tools

def EndStudySession(): # Writes the response to summaryPrompt into the StudyHistory.txt file
    print('\nEnding study session...')

    Sensors.StopSensors()

    with open('./KB/StudyHistory.txt', 'a') as f1, open('./Prompts/SummaryPrompt.txt', 'r') as p: 
        print('Generating Summary...')
        summary = SLMResponse.PromptAI(Tools.ReadFileAsLine(p))
        f1.write('\n' + summary) # Prompt Summary, append it to history file
        print(summary)
    with open('./KB/StudyHistory.txt', 'r') as f1, open('./KB/Knowledge.txt', 'w') as f2, open('./Prompts/KnowledgePrompt.txt', 'r') as p:
        # global context
        # context = [] # reset the context

        f2.truncate(0) # Replace old knowledge with new knowledge
        print('Generating Knowledge...')
        knowledge = SLMResponse.PromptAI(Tools.ReadFileAsLine(f1) + Tools.ReadFileAsLine(p))
        f2.write(knowledge)
        print(knowledge)

    # print('Clearing old knowledge base files...')
    # for i in API.KBIDs: API.delete_knowledge(i) # Delete knowledge bases
    # subprocess.run("rm ./.open-webui/uploads/*", shell=True) # Delete uploaded files
    # subprocess.run("cd ./.open-webui/vector_db && rm -r `ls | grep -v 'chroma.sqlite3'`", shell=True) # except this file its required idk

    print("\nExiting FOCUS...\n")


def T_GUI(): import GUI # Start the GUI

def T_Sensors():
    Sensors.StartSensors()

    while True: # Main sensor loop
        sensorData = Sensors.Sense()
        print(sensorData)

        detect = SLMResponse.DistractionDetection(sensorData)

        # if detect == 'yes': 
        #     GUI.chat._insert_ai("You seem to be distracted, perhaps try one of the actions to get back on track.")

        if detect == 'yes': # Temp for testing, since we cant call the chat func from here
            print("Distraction detected!")

        time.sleep(Sensors.iterDelay)


# Main 2 threads, one for sensors and 1 for the GUI
try: 
    t_sensors = threading.Thread(target=T_Sensors)
    t_GUI = threading.Thread(target=T_GUI)

    t_GUI.start()
    input("Press Enter to continue")
    t_sensors.start()

    t_GUI.join()
    t_sensors.join()

except KeyboardInterrupt:
    EndStudySession()

print("\n\nFOCUS exiting...")