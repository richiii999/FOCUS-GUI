import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

import time

from modules import Sensors


try:
    Sensors.StartSensors()
    while True: 
        print(Sensors.Sense())
        time.sleep(Sensors.iterDelay)

except KeyboardInterrupt: Sensors.StopSensors()