# Sensors.py
# Tests if ffmpeg works, and if the sensors will turn on and log correctly.

import sys
import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

def EndStudySession(): # Writes the response to summaryPrompt into the StudyHistory.txt file
    print('\nEnding study session...')

    print('Stopping sensors...')
    ffmpeg.terminate()
    for s in sensors[1:]: s.terminate()
    for f in procs.values(): f.close() 

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

try:
    print("Starting sensors...") # Sensor processes which record data to be passed to the AI
    sensors = [subprocess.Popen(path.split(), stderr=subprocess.DEVNULL, stdout=log, stdin=subprocess.DEVNULL) for path,log in procs.items()]
finally:
    EndStudySession()