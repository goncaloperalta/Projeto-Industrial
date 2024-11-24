import shared_memory as sh
from numpy import (random, linspace)

def SensorReader():
    while True:
        sh.sem_SSH_ready.acquire()      # Wait for the a SSH connection
        
        print("\033[95m[SENSOR] Generating random values...\033[00m")
        sh.readings = {}                # Reset the old readings

        # Code to read the sensor goes here
        # just sending random data for now...
        sh.readings['val'] = [random.randint(1, 10) for _ in range(11)]
        sh.readings['time'] = linspace(0, 10, 11).tolist()
        
        print("\033[95m[SENSOR] Readings ready\033[00m")
        sh.sem_readings_ready.release() # Signal the API that the Readings are ready to send
