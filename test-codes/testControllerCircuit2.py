# Pin 11 (board mode): H-Bridge (enable)
# Pin 13 (board mode): Current Sensor (Reset)
# Pin 12 (board mode): H-Bridge (Forward)
# Pin 32 (board mode): H-Bridge (Reverse)
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

ENABLE = 11
RESET = 13
FORWARD = 12
REVERSE = 32

# Enable Pin
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.output(ENABLE, GPIO.LOW) 	# Disabled 
GPIO.setup(ENABLE, GPIO.IN) 	# Enabled (Open drain)

# Reset Pin
GPIO.setup(RESET, GPIO.OUT)
#GPIO.output(RESET, GPIO.LOW)	# Deactivates the current sensor circuit
GPIO.output(RESET, GPIO.HIGH)	# Activates the current sensor circuit

# PWM Forward Pin 
GPIO.setup(FORWARD, GPIO.OUT)		# Controls the Actuator in one direction
pFORWARD = GPIO.PWM(FORWARD, 8000)	# 1 kHz
pFORWARD.start(0)

# PWM Reverse Pin
GPIO.setup(REVERSE, GPIO.OUT)		# Controls the Actuator in the oposite direction
#GPIO.output(REVERSE, GPIO.LOW)
pREVERSE = GPIO.PWM(REVERSE, 8000)	# 1 kHz
pREVERSE.start(0)


for i in range(5):
	# Forward
	pFORWARD.ChangeDutyCycle(50)

	sleep(5)

	pFORWARD.ChangeDutyCycle(0)

	GPIO.output(RESET, GPIO.LOW)

	# Reverse
	pREVERSE.ChangeDutyCycle(75)

	sleep(3)

	pREVERSE.ChangeDutyCycle(0)

	GPIO.output(RESET, GPIO.HIGH)

# Clean
pREVERSE.stop()
pFORWARD.stop()
GPIO.cleanup()
