# Pin 11 (board mode): H-Bridge (Enable)
# Pin 13 (board mode): Current Sensor (Reset)
# Pin 12 (board mode): H-Bridge (IN_A)
# Pin 32 (board mode): H-Bridge (IN_B)

# Enable signal
# Floating   -> asks for enabling, read to see if agreed
# Pulled LOW -> forced disabling

# Reset signal
# HIGH -> Current Limiter latches       - hard enabled
# LOW  -> Current Limiter doesn't latch - fuzzy disabled

# Driving IN signals
#  A      B
# LOW    LOW  Braking
# LOW   HIGH  One way
# HIGH   LOW  Other way
# HIGH  HIGH  Braking


import RPi.GPIO as GPIO
import shared_memory as sh
from time import sleep


ENABLE = 11
RESET = 13
INA = 12
INB = 32


def ControlCode():

    sh.profile["duration"] = 1
    # sh.profile["interval"] = 1
    # sh.profile["times"] = 5


    # GPIO.setmode(GPIO.BOARD)

    # # Enable Pin
    # GPIO.setup(ENABLE, GPIO.OUT)    # Saving Pull Down State
    # GPIO.output(ENABLE, GPIO.LOW)
    # GPIO.setup(ENABLE, GPIO.IN)         # Defaulting Enabled

    # # Reset Pin
    # GPIO.setup(RESET, GPIO.OUT)
    # GPIO.output(RESET, GPIO.HIGH)

    # # Setup the two driving signals
    # GPIO.setup(INA, GPIO.OUT)
    # pINA = GPIO.PWM(INA, 1000)
    # pINB.start(0)

    # GPIO.setup(INB, GPIO.OUT)
    # pINA = GPIO.PWM(INB, 1000)
    # pINB.start(0)

    # while True:
    #     # wait for signal to start
    #     sh.sem_SSH_ready.acquire()

    #     print("\033[93m[CONTROL] Starting\033[00m")

    #     # enable controller
    #     GPIO.setup(ENABLE, GPIO.IN);


    #     for i in range(sh.profile["times"]):
    #         print(f"\033[93m[CONTROL] On {i} press\033[00m")

    #         # clear up possible stray state on current limiter
    #         GPIO.output(RESET, GPIO.LOW)
    #         sleep(0.001)
    #         GPIO.output(RESET, GPIO.HIGH)

    #         # start extending
    #         pINA.ChangeDutyCycle(50)
    #         pINB.ChangeDutyCycle(0)

    #         # wait for force to reach the clicking force
    #         for k in range(round(5/0.05)):
    #             sleep(0.05)
    #             if sh.readings["val"][len(sh.readings["val"])-1] > 4:
    #                 print("\033[93m[CONTROL] Reached clicking force\033[00m")
    #                 break

    #             elif GPIO.input(ENABLE) == 0 :
    #                 print("\033[91m[CONTROL] Current limit reached before clicking force\033[00m")
    #                 GPIO.output(RESET, GPIO.LOW)
    #                 sleep(0.001)
    #                 GPIO.output(RESET, GPIO.HIGH)

    #             elif k == round(5/0.05) :
    #                 print("\033[91m[CONTROL] Couldn't reach clicking force\033[00m"


    #         # brake and hold
    #         pINA.ChangeDutyCycle(0)
    #         pINB.ChangeDutyCycle(0)
    #         sleep(sh.profile["duration"])

    #         # retract
    #         pINA.ChangeDutyCycle(0)
    #         pINB.ChangeDutyCycle(50)

    #         GPIO.output(RESET, GPIO.LOW)    # limiter still on in case it's going the wrong way
    #         sleep(0.001)
    #         GPIO.output(RESET, GPIO.HIGH)

    #         sleep(1)
    #         pINA.ChangeDutyCycle(0)
    #         pINB.ChangeDutyCycle(0)


    #         # pause between presses
    #         sleep(sh.profile["interval"])


    #     # disable controller
    #     GPIO.setup(ENABLE, GPIO.IN);


    # pREVERSE.stop()
    # pFORWARD.stop()
    # GPIO.cleanup()
