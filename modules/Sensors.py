# Sensors.py
# Starts ffmpeg + sensors via subprocess

import time
import subprocess # manages subprocess I/O (ollama / webui servers, sensors, and ffmpeg)

startTime, initDelay, iterDelay = time.time(), 5, 10 # Timing delays

ffmpeg = None # Set on StartSensors()
sensors = None # BUG: suddenly stopped working idk

procs = { # {path : Log file}, sensor output is periodically read from here and given to the AI
    'python ./Sensors/PythonFaceTracker/main.py'    : open('./SensorLogs/faceTracker.txt', 'r+'),
    'python ./Sensors/PythonGazeTracker/example.py' : open('./SensorLogs/gazeTracker.txt', 'r+')
}

for f in procs.values(): 
    f.truncate(0) # Empty old logs
    f.write('The user seems focused\n') # Placeholder first log entry

def StopSensors():
    global ffmpeg
    global sensors
    print('Stopping sensors...')
    if ffmpeg is not None: ffmpeg.terminate()
    if sensors is not None: 
        for s in sensors[1:]: s.terminate()
    for f in procs.values(): f.close() 

def Sense() -> str: # Gather output from the sensors
    sensorData = f"Time = {int(time.time() - startTime)}, aggregated Sensor data:\n"
    for f in procs.values(): # Get most recent output per sensor 
        if not f.closed:
            f.seek(0)
            sensorData += f.readlines()[-1]
    return sensorData

def StartSensors():
    global ffmpeg
    global sensors
    print("Starting FFMPEG...") ### Sensors & Subprocesses # Setup virtual cam devices and split original cam input to them
    ffmpeg = subprocess.Popen('ffmpeg  -i /dev/video0 -f v4l2 -vcodec rawvideo -s 640x360 /dev/video8 -f v4l2 -vcodec rawvideo -s 640x360 /dev/video9 -loglevel quiet'.split(), stdin=subprocess.DEVNULL)
    time.sleep(2) # Couple sec buffer for ffmpeg to start 

    print("Starting Sensors...") # Sensor processes which record data to be passed to the AI
    sensors = [subprocess.Popen(path.split(), stderr=subprocess.DEVNULL, stdout=log, stdin=subprocess.DEVNULL) for path,log in procs.items()]
