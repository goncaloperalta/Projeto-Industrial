# Cable color:  [from RPI -> to PCB] 
# Purple:       [3V3 -> TP1] 
# Black:        [SDA -> TP5]
# Gray:         [SCL -> TP4]
# White:        [GND -> TP3]

#python testSensor2.py


# S1 S0 B13..B8 | B7..B0 | T10..T3 | T2..T1




from smbus2 import SMBus
from time import sleep

fmax = round(0.8 * (2**14-1))
fmin = round(0.2 * (2**14-1))
frated = 15

i = 0
with SMBus(1) as bus:
    while i < 120:
        bytes = bus.read_i2c_block_data(0x28, 0, 4)
        word = bytes[3] + (bytes[2] << 8) + (bytes[1] << 16) + (bytes[0] << 24)

        tempdata = (word & 0x0000FFE0) >> 5
        temp = (tempdata * 200/2047) - 50
        
        forcedata = (word & 0x3FFF0000) >> 16
        force = frated*(forcedata-fmin)/(fmax-fmin)

        print(f"force: {force:2.2f} N  {force/0.00981:4.0f} g | temperature: {temp:2.2f} C")

        i = i + 1
        sleep(0.5)
