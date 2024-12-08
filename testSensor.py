# Cable color:  [from RPI -> to PCB] 
# Purple:       [3V3 -> TP1] 
# Black:        [SDA -> TP5]
# Gray:         [SCL -> TP4]
# White:        [GND -> TP3]

from smbus2 import SMBus
from time import sleep

OutputMAX = 0.8 * 2**14
OutputMIN = 0.2 * 2**14
ForceRated = 15
Force = 0

i = 0
with SMBus(1) as bus:
        while i < 10:
                bytes = bus.read_i2c_block_data(0x28, 0, 2)
                Output = (bytes[0] << 8) + bytes[1];
                Force = (Output-OutputMIN)*ForceRated/(OutputMAX-OutputMIN)
                print(f"Force: {round(Force*100)/100} N | Weight: {round(Force/10*1000)/1000} Kg")
                print("----")
                i = i + 1
                sleep(1)