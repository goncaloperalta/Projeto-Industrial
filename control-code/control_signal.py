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

import logging
from time import sleep
import RPi.GPIO as GPIO # type: ignore
import shared_memory as sh

logger = logging.getLogger("CONTROL CODE")

ENABLE = 11
RESET = 13
INA = 12
INB = 32

def ControlCode():
    GPIO.setmode(GPIO.BOARD)
    # Enable Pin
    GPIO.setup(ENABLE, GPIO.OUT)    # Saving Pull Down State
    GPIO.output(ENABLE, GPIO.LOW)
    GPIO.setup(ENABLE, GPIO.IN)     # Defaulting Enabled
    # Reset Pin
    GPIO.setup(RESET, GPIO.OUT)
    GPIO.output(RESET, GPIO.LOW)
    # Setup the two driving signals
    GPIO.setup(INA, GPIO.OUT)
    pINA = GPIO.PWM(INA, 8000)
    pINA.start(0)
    GPIO.setup(INB, GPIO.OUT)
    pINB = GPIO.PWM(INB, 8000)
    pINB.start(0)

    while True:
        # Control Signal Loop
        # 1 - Wait for start
        # 2 - Extend the Actuator
        # 3 - Wait for a call from the sensor
        # 4 - Hold of the specified time
        # 5 - Retract the actuator
        # Repeat
        
        # wait for start signal 
        sh.startSensorAndControl.acquire()
        
        with sh.access:
            holdTime = sh.parameters.pressTime
        print("\033[93m[CONTROL] Starting\033[00m")
        logging.info("Enabling controller circuit")

        # enable controller
        GPIO.setup(ENABLE, GPIO.IN)

        # clear up possible stray state on current limiter
        #GPIO.output(RESET, GPIO.LOW)
        #sleep(0.001)
        #GPIO.output(RESET, GPIO.HIGH)

        # start extending
        logger.info("Extending Actuator")
        pINA.ChangeDutyCycle(15)
        pINB.ChangeDutyCycle(0)

        # wait for press
        sh.buttonPressed.acquire()

        # brake and hold
        pINA.ChangeDutyCycle(0)
        pINB.ChangeDutyCycle(0)
        logger.info(f"Holding Actuator position for {holdTime} seconds")
        sleep(holdTime)
                
        # retract
        logger.info("Retracting Actuator")
        pINA.ChangeDutyCycle(0)
        pINB.ChangeDutyCycle(50)

        #GPIO.output(RESET, GPIO.LOW)    # limiter still on in case it's going the wrong way
        #sleep(0.001)
        #GPIO.output(RESET, GPIO.HIGH)

        sleep(0.5)
        pINA.ChangeDutyCycle(0)
        pINB.ChangeDutyCycle(0)

        logger.info("Disabling controller circuit")
        # disable controller
        GPIO.setup(ENABLE, GPIO.IN);

    # Never reaches here
    pINA.stop()
    pINB.stop()
    GPIO.cleanup()
