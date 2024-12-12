from smbus2 import SMBus
from time import (sleep, perf_counter)
import shared_memory as sh
from numpy import (random, linspace)

OutputMAX = 0.8 * 2**14
OutputMIN = 0.2 * 2**14
ForceRated = 15
Force = 0

def SensorReader():
    while True:
        sh.sem_SSH_ready.acquire()      # Wait for the a SSH connection

        print("\033[95m[SENSOR] Generating random values...\033[00m")
        sh.readings = {}                # Reset the old readings
        tic = perf_counter()
        print("\033[95m[SENSOR]" + str(tic) + "\033[00m")
        i = 0
        ForceArr = []
        with SMBus(1) as bus:
            while i < 75:
                bytes = bus.read_i2c_block_data(0x28, 0, 2)
                Output = (bytes[0] << 8) + bytes[1];
                Force = (Output-OutputMIN)*ForceRated/(OutputMAX-OutputMIN)
                print(f"Force: {round(Force*100)/100} N | Weight: {round(Force/10*1000)/1000} Kg")
                print("----")
                i = i + 1
                sleep(0.05)
                ForceArr.append(Force)

        toc = perf_counter()
        time = toc-tic
        time = linspace(0, time, len(ForceArr))
        sh.readings['val'] = ForceArr
        sh.readings['time'] = time.tolist()

        print(sh.readings)
        print("\033[95m[SENSOR] Readings ready\033[00m")
        sh.sem_readings_ready.release() # Signal the API that the Readings are ready to send
