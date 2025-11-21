# Main.py

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

import API # Contains API calls to webui

def EndStudySession(): # Writes the response to summaryPrompt into the StudyHistory.txt file
    print('\nEnding study session...')

    print('Stopping sensors...')
    ffmpeg.terminate() # ffmpeg sometimes doesnt terminate, so just spam it 
    for s in sensors[1:]: s.terminate()
    for f in procs.values(): f.close() 

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

    print("\nExiting...\n")

def Sense() -> str: # Gather output from the sensors
    sensorData = f"Time = {int(time.time() - startTime)} minutes, Aggregated Sensor data:\n"
    for f in procs.values(): # Get most recent output per sensor 
        f.seek(0)
        sensorData += f.readlines()[-1]
    return sensorData

startTime, initDelay, iterDelay = time.time(), 3, 5 # Timing delays

print("Starting FFMPEG...") ### Sensors & Subprocesses # Setup virtual cam devices and split original cam input to them
ffmpeg = subprocess.Popen('ffmpeg  -i /dev/video0 -f v4l2 -vcodec rawvideo -s 640x360 /dev/video8 -f v4l2 -vcodec rawvideo -s 640x360 /dev/video9 -loglevel quiet'.split(), stdin=subprocess.DEVNULL)
time.sleep(2) # Couple sec buffer for ffmpeg to start 

procs = { # {path : Log file}, sensor output is periodically read from here and given to the AI
    'python ./Sensors/PythonFaceTracker/main.py'    : open('./SensorLogs/faceTracker.txt', 'r+'),
    'python ./Sensors/PythonGazeTracker/example.py' : open('./SensorLogs/gazeTracker.txt', 'r+')
}

for f in procs.values(): 
    f.truncate(0) # Empty old logs
    f.write('The user seems focused\n') # Placeholder first log entry

print("Starting sensors...") # Sensor processes which record data to be passed to the AI
sensors = [subprocess.Popen(path.split(), stderr=subprocess.DEVNULL, stdout=log, stdin=subprocess.DEVNULL) for path,log in procs.items()]


import GUI # Start the GUI