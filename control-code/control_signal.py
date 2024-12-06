import RPi.GPIO as GPIO
import shared_memory as sh
from time import sleep

def ControlCode():
    while True:
        sh.sem_SSH_ready.acquire()
        print("\033[93m[CONTROL]\033[00m")

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(12, GPIO.OUT)
        # p = GPIO.PWM(12, 0.5)
        # p.start(1)  # Turn on Motor
        
        # # Wait for feedback
        # sh.sem_feedback_ready.acquire()

        # p.stop()
        
        # # Retrieve
        # GPIO.setup(13, GPIO.OUT)
        # GPIO.output(13, GPIO.HIGH)
        # sleep(3)
        # GPIO.cleanup()