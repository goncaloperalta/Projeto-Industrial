import shared_memory as sh
from numpy import (random, linspace)
from threading import Semaphore
from time import sleep

def SensorReader():
    while True:
        print("[SENSOR] Waiting for an API request...")
        sh.sem_SSH_ready.acquire()      # Wait for the a SSH connection
        
        print("[SENSOR] Generating random values...")
        sh.readings = {}                # Reset the old readings

        # Code to read the sensor goes here
        # just sending random data for now...
        sh.readings['val'] = [random.randint(1, 10) for _ in range(10)]
        sh.readings['time'] = linspace(0, 10, 11).tolist()
        sleep(2)
        
        print("[SENSOR] Readings ready")
        sh.sem_readings_ready.release() # Signal that the Readings are ready to send
