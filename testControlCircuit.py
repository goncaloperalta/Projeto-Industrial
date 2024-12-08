# Pin 11 (board mode): H-Bridge (enable) 
# Pin 13 (board mode): H-Bridge (Forward)
# Pin 15 (board mode): H-Bridge (Reverse)

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)    # Enable (Open drain)
GPIO.setup(13, GPIO.OUT)    # Forward
GPIO.setup(15, GPIO.OUT)    # Reverse

# Forward
forward = GPIO.PWM(12, 1000)   # 1kHz freq
forward.ChangeDutyCycle(0.5)
# forward.ChangeFrequence(1000)

forward.start(1)  # Turn on Motor
sleep(3)
forward.stop()    # Stop

# Reverse
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
sleep(3)

GPIO.cleanup()