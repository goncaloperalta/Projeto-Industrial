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
        sh.startSensorAndControl.acquire()      # Wait for the SSH connection

        flag = 0
        holdTime = 0
        sh.readings = {}                # Reset old readings
        sh.readings['val'] = []         # Reset old force values
        sh.readings['time'] = []        # Reset old time values
        print("\033[95m[SENSOR] Starting to read from force sensor\033[00m")
        logger.info("Starting to read from force sensor")

        tic = perf_counter()    # Start counting time
        tic2 = perf_counter()

        with SMBus(1) as bus:
            while True:
                bytes = bus.read_i2c_block_data(0x28, 0, 2)
                Output = (bytes[0] << 8) + bytes[1];
                Force = (Output-OutputMIN)*ForceRated/(OutputMAX-OutputMIN)
                if Force < 0:   # Sensor gives -0.15 as the lowest value
                    Force = 0
                sh.readings['val'].append(round(Force, 4))    

                if flag == 0:
                    if Force > 5: # If more than 5 newtons are read stop the actuator
                        with sh.access:
                            sh.PRESSED = True
                            holdTime = sh.parameters.pressTime
                        flag = 1
                        tic2 = perf_counter()
                        sh.buttonPressed.release(2)
                    
                    if (perf_counter() - tic) > 5:  # Timeout 5 sec
                        sh.buttonPressed.release(2)
                        break

                elif perf_counter() - tic2 > tic2 + holdTime:
                    break;
                        
                sleep(0.01)
        
        if flag:
            time = linspace(0, perf_counter()-tic, len(sh.readings['val'])).tolist()
            sh.readings['time'] = [round(el, 3) for el in time]

        print("\033[95m[SENSOR] Readings ready\033[00m")
        logging.info("Force readings ready")
        sh.sensorReadingsReady.release() # Signal the API that the Force readings are ready to be sent
