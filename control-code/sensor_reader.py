import logging
import threading
from smbus2 import SMBus # type: ignore
from numpy import linspace
import shared_memory as sh
from time import (sleep, perf_counter)

logger = logging.getLogger(__name__)

OutputMAX = 0.8 * 2**14
OutputMIN = 0.2 * 2**14
ForceRated = 15
Force = 0

def breakSensorLoop():
    sh.sem_feedback_ready.acquire()     # Wait for feedback ready
    sh.stopSensor = 1

def SensorReader():
    while True:
        sh.sem_SSH_ready.acquire()      # Wait for the SSH connection

        flag = 0
        sh.readings = {}                # Reset old readings
        sh.readings['val'] = []         # Reset old force values
        sh.readings['time'] = []        # Reset old time values
        print("\033[95m[SENSOR] Starting to read from force sensor\033[00m")
        logger.info("Starting to read from force sensor")

        tic = perf_counter()    # Start counting time
        threading.Thread(target=breakSensorLoop).start()    # Thread to wait for a feedback

        with SMBus(1) as bus:
            while True:
                bytes = bus.read_i2c_block_data(0x28, 0, 2)
                Output = (bytes[0] << 8) + bytes[1];
                Force = (Output-OutputMIN)*ForceRated/(OutputMAX-OutputMIN)
                sleep(0.01)

                if Force < 0:   # Sensor gives -0.15 as the lowest value
                    Force = 0
                
                if flag == 0 and Force > 2: # If more than 2 newtons are read stop the actuator
                    flag = 1
                    sh.sem_force_read.release()
                sh.readings['val'].append(round(Force, 4))

                if sh.stopSensor == 1:
                    sh.stopSensor = 0
                    break

        toc = perf_counter()    # Stop time counter
        time = linspace(0, toc-tic, len(sh.readings['val'])).tolist()
        sh.readings['time'] = [round(el*100)/100 for el in time]

        print("\033[95m[SENSOR] Readings ready\033[00m")
        logging.info("Force readings ready")
        sh.sem_readings_ready.release() # Signal the API that the Force readings are ready to be sent
