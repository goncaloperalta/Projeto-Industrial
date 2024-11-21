import json
from numpy import random
from numpy import linspace
from requests import post
from threading import Semaphore
import shared_memory as sh
from time import sleep

def SensorReader():
    while True:
        sh.sem_SSH_ready.acquire()      # Wait for the a SSH connection
        
        sh.readings = {}                # Reset the old readings

        # Code to read the sensor goes here
        # just sending random data for now...
        sh.readings['val'] = [random.randint(1, 10) for _ in range(10)]
        sh.readings['time'] = linspace(0, 10, 11).tolist()
        sleep(2)
        
        sh.sem_readings_ready.release() # Signal that the Readings are ready to send
