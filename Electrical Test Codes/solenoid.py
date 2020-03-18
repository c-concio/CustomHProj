import sleep
import RPI.GPIO as GPIO

# ---------------------------------------------------------------
#                       Variable Changes

solPin1 = 4
solPin2 = 14

# ---------------------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setup(solPin1, GPIO.OUT)
GPIO.setup(solPin2, GPIO.OUT)

GPIO.output(solPin1, GPIO.HIGH)
GPIO.output(solPin2, GPIO.HIGH)

sleep(5)

GPIO.output(solPin1, GPIO.LOW)
GPIO.output(solPin2, GPIO.LOW)

print("GPIO off")

GPIO.cleanup()