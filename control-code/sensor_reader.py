import json
from numpy import random
from numpy import linspace
from requests import post
from threading import Semaphore
from semaphores import sem_api

def SensorReader():
    while True:
        sem_api.acquire()
        
        x = {}
        x['val'] = [random.randint(1, 10) for _ in range(10)]
        x['time'] = linspace(0, 10, 11).tolist()
        post("http://localhost:8000/sensor_readings", json=x)