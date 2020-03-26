import time
import RPI.GPIO as GPIO

# ---------------------------------------------------------------
#                       Variable Changes

# rotation = "forward" or "backward"
rotation = "forward"
dirPin = 6
stepPin = 12
stepsPerRevolution = 200
delay = 0.001

# ---------------------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)

if rotation == "forward":
	GPIO.output(dirPin, 1)
else:
	GPIO.output(dirPin, 0)

for i in range(stepsPerRevolution):
	GPIO.output(stepPin, GPIO.HIGH)
	sleep(delay)
	GPIO,output(stepPin, GPIO.LOW)
	sleep(delay)

GPIO.cleanup()