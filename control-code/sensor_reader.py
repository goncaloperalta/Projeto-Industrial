import logging
import threading
from smbus2 import SMBus # type: ignore
from numpy import linspace
import shared_memory as sh
from time import (sleep, perf_counter)

logger = logging.getLogger("SENSOR")

OutputMAX = 0.8 * 2**14
OutputMIN = 0.2 * 2**14
ForceRated = 15
Force = 0

def SensorReader():
    while True:
        # Sensor Loop
        # 1 - Wait for start
        # 2 - Get the pressTime parameter
        # 3 - Store current time
        # 4 - Read force values
        # 5 - If force is greater than a threshold read for the pressTime and 2 more seconds
        # 6 - Store the results on the shared dictionary
        # 7 - Resume the state module
        # Repeat
        
        sh.startSensorAndControl.acquire()      # Wait for the SSH connection
        logger.info("Sensor module started")

        flag = 0
        with sh.access:
            holdTime = sh.parameters.pressTime
            sh.modulesData['force_val'] = []
            sh.modulesData['time_val'] = []

        print("\033[95m[SENSOR] Starting to read from force sensor\033[00m")
        logger.info("Starting to read from force sensor")

        tic = perf_counter()    # Start counting time
        tic2 = perf_counter()

        with SMBus(1) as bus:
            while True:
                try:
                    bytes = bus.read_i2c_block_data(0x28, 0, 2)
                except OSError:
                    with sh.access:
                        sh.ERROR = 'SENSOR'
                    bytes = [1, 1]
                Output = (bytes[0] << 8) + bytes[1];
                Force = (Output-OutputMIN)*ForceRated/(OutputMAX-OutputMIN)
                if Force < 0:   # Sensor gives -0.15 as the lowest value
                    Force = 0

                with sh.access:
                    sh.modulesData['force_val'].append(round(Force, 4))

                if flag == 0:
                    if Force > 2: # If more than 5 newtons are read stop the actuator
                        logger.info("Sensed force greater than 5 Newtons")
                        with sh.access:
                            sh.PRESSED = True
                        flag = 1
                        tic2 = perf_counter()
                        sh.buttonPressed.release(2)
                    
                    if (perf_counter() - tic) > 5:  # Timeout 5 sec
                        logger.info("Timed out")
                        sh.buttonPressed.release(2)
                        break

                elif perf_counter() > (tic2 + holdTime + 2):
                    logger.info("Stoped reading")
                    break
                sleep(0.01)
        
        if flag:
            time = linspace(0, perf_counter()-tic, len(sh.modulesData['force_val'])).tolist()
            sh.modulesData['time_val'] = [round(el, 3) for el in time]

        print("\033[95m[SENSOR] Readings ready\033[00m")
        logging.info("Force readings ready")
        sh.sensorReadingsReady.release()
