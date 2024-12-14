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
import threading
from time import sleep
import RPi.GPIO as GPIO
import shared_memory as sh

logger = logging.getLogger(__name__)

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
    GPIO.output(RESET, GPIO.HIGH)
    # Setup the two driving signals
    GPIO.setup(INA, GPIO.OUT)
    pINA = GPIO.PWM(INA, 1000)
    pINA.start(0)
    GPIO.setup(INB, GPIO.OUT)
    pINB = GPIO.PWM(INB, 1000)
    pINB.start(0)

    while True:
        # wait for signal to start
        logging.info("Waiting for a call")
        sh.sem_SSH_ready.acquire()
        print("\033[93m[CONTROL] Starting\033[00m")
        logging.info("Starting")

        # enable controller
        GPIO.setup(ENABLE, GPIO.IN)

        # clear up possible stray state on current limiter
        GPIO.output(RESET, GPIO.LOW)
        sleep(0.001)
        GPIO.output(RESET, GPIO.HIGH)

        # start extending
        pINA.ChangeDutyCycle(50)
        pINB.ChangeDutyCycle(0)

        # wait for press
        # threading.Thread(target=checkForce).start()
        sh.sem_feedback_ready.acquire()

        # brake and hold
        pINA.ChangeDutyCycle(0)
        pINB.ChangeDutyCycle(0)
        logger.info("Holding position")
        sleep(1)

        # retract
        logger.info("Retracting")
        pINA.ChangeDutyCycle(0)
        pINB.ChangeDutyCycle(75)

        GPIO.output(RESET, GPIO.LOW)    # limiter still on in case it's going the wrong way
        sleep(0.001)
        GPIO.output(RESET, GPIO.HIGH)

        sleep(3)
        pINA.ChangeDutyCycle(0)
        pINB.ChangeDutyCycle(0)

        # disable controller
        GPIO.setup(ENABLE, GPIO.IN);

    # Never reaches here
    pINA.stop()
    pINB.stop()
    GPIO.cleanup()
