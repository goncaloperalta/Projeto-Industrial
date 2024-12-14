from smbus2 import SMBus
from time import (sleep, perf_counter)
import shared_memory as sh
from numpy import (random, linspace)
import threading
import logging

logger = logging.getLogger(__name__)

OutputMAX = 0.8 * 2**14
OutputMIN = 0.2 * 2**14
ForceRated = 15
Force = 0

def breakSensorLoop():
    print("\033[95m[SENSOR] Waiting for a button feedback...\033[00m")
    logger.info("Waiting for a button feedback...")
    sh.sem_feedback_ready.acquire()     # Wait for feedback ready
    sh.stopSensor = 1
    print("\033[95m[SENSOR] Got a button feedback\033[00m")
    logger.info("Got a button feedback")

def SensorReader():
    while True:
        sh.sem_SSH_ready.acquire()      # Wait for the a SSH connection
        print("\033[95m[SENSOR] Starting to read from sensor...\033[00m")
        logger.info("Starting to read from sensor...")

        sh.readings = {}                # Reset old readings
        ForceArr = []                   # Reset old force values

        tic = perf_counter()
        threading.Thread(target=breakSensorLoop).start()
        with SMBus(1) as bus:
            while True:
                bytes = bus.read_i2c_block_data(0x28, 0, 2)
                Output = (bytes[0] << 8) + bytes[1];
                Force = (Output-OutputMIN)*ForceRated/(OutputMAX-OutputMIN)
                #print(f"Force: {round(Force*100)/100} N | Weight: {round(Force/10*1000)/1000} Kg")
                #print("----")
                sleep(0.05)
                if Force < 0:
                    Force = 0
                ForceArr.append(round(Force*10)/10)
                if sh.stopSensor == 1:
                    sh.stopSensor = 0
                    break

        toc = perf_counter()
        time = linspace(0, toc-tic, len(ForceArr)).tolist()
        sh.readings['val'] = ForceArr
        sh.readings['time'] = [round(el*100)/100 for el in time]

        print("\033[95m[SENSOR] Readings ready\033[00m")
        logging.info("Readings ready")
        sh.sem_readings_ready.release() # Signal the API that the Readings are ready to send
