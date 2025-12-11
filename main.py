# Main.py

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)
import threading # Multithread the sensors and GUI separately

import API # Contains API calls to webui
from modules import Sensors # Controls the face+gaze trackers
import SLMResponse # Model controls

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


def T_GUI():
    import GUI # Start the GUI

def T_Sensors():
    try:
        Sensors.StartSensors()
        while True: 
            sensorData = Sensors.Sense()
            print(sensorData)

            detect = SLMResponse.DistractionDetection(sensorData)

            # if detect == 'yes': 
            #     GUI.chat._insert_ai("You seem to be distracted, perhaps try one of the actions to get back on track.")

            if detect == 'yes': # Temp for testing, since we cant call the chat func from here
                print("Distraction detected!")

            time.sleep(Sensors.iterDelay)

    except KeyboardInterrupt: Sensors.StopSensors()

# Main 2 loops, one for sensors and 1 for the GUI
t_sensors = threading.Thread(target=T_Sensors)
t_GUI = threading.Thread(target=T_GUI)

t_GUI.start()
input("Press Enter to continue")
t_sensors.start()

t_sensors.join()
t_GUI.join()

print("\n\nFOCUS exiting...")