# Pin 11 (board mode): H-Bridge (enable)
# Pin 13 (board mode): H-Bridge (Forward)
# Pin 15 (board mode): H-Bridge (Reverse)

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# Enable
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
GPIO.setup(11, GPIO.IN)

# Reset
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH) # D

# PWM Forward
GPIO.setup(12, GPIO.OUT)

# PWM Reverse
GPIO.setup(32, GPIO.OUT)
GPIO.output(32, GPIO.LOW)

p12 = GPIO.PWM(12, 1000)
p12.start(0)
p32 = GPIO.PWM(32, 1000)
p32.start(0)

for i in range(5):
	# Forward
	p12.ChangeDutyCycle(50)

	#GPIO.output(13, GPIO.HIGH) # D
	#sleep(1)
	#GPIO.output(13, GPIO.LOW) # A
	#sleep(1)
	#GPIO.output(13, GPIO.HIGH) # D
	#sleep(1)
	#GPIO.output(13, GPIO.LOW) # A
	#sleep(1)

	#GPIO.setup(11, GPIO.IN)
	#sleep(1)
	#print(GPIO.input(11))
	#GPIO.setup(11, GPIO.OUT)
	#sleep(1)
	#GPIO.setup(11, GPIO.IN)
	#sleep(1)
	#print(GPIO.input(11))
	#GPIO.setup(11, GPIO.OUT)
	#sleep(1)
	#GPIO.setup(11, GPIO.IN)
	#print(GPIO.input(11))

	sleep(5)

	p12.ChangeDutyCycle(0)

	GPIO.output(13, GPIO.LOW)

	# Reverse
	p32.ChangeDutyCycle(75)

	sleep(3)

	p32.ChangeDutyCycle(0)

	GPIO.output(13, GPIO.HIGH)

p32.stop()
p12.stop()

GPIO.cleanup()
