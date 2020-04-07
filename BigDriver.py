import time
import RPi.GPIO as GPIO
import i2c_initial_setup as setup

dirPin = 7  # direction pin     0: Forward  1: Backward

stepPin1 = 8  # step GPIO pin
stepPin2 = 10  # step GPIO pin
stepPin3 = 12  # step GPIO pin
stepPin4 = 11  # step GPIO pin
stepPin5 = 13  # step GPIO pin
stepPin6 = 15  # step GPIO pin
stepPin7 = 19  # step GPIO pin
stepPin8 = 21  # step GPIO pin
stepPin9 = 23  # step GPIO pin
stepPin10 = 32  # step GPIO pin
stepPin11 = 36  # step GPIO pin
stepPin12 = 38  # step GPIO pin
stepPinMix = 3
stepPinClean = 5

enablePin = 37

CW = 1  # clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 287 * 200  # Steps per revolution (360 / 1.8)

GPIO.setup(dirPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin5, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin6, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin9, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPinMix, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPinClean, GPIO.OUT, initial=GPIO.LOW)

timeDelay = 0.01

"""
Work in term of the decoder
stepPin also means which ID of the cylinder.
"""

def mix():
    driveBigMotorForward(stepPinMix, 30)

def driveBigMotorForward(stepPin, step):
    binaryStringStepPin = format(stepPin, '#06b')
    binaryNumArrayStepPin = list(binaryStringStepPin)

    # Select line that goes through the select lines from the DEMUX to select correct driver.
    # GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)     # Makes sure that it doesn't run at the beginning.

    GPIO.output(enablePin, GPIO.HIGH)

    for i in range(0, step):

        """
        Will use 1 pin for all Direction Pins, we don't really care if we set all of Forward or Backwards
        Will use 3 or 4 select pins for Step Pins and 1 other pin to choose on or off. Possibility of using 4 or 5 pins in total 
        """

        # Forward drive block
        GPIO.output(dirPin, GPIO.LOW)
        GPIO.output(stepPin, GPIO.HIGH)

        time.sleep(timeDelay)

        GPIO.output(dirPin, GPIO.LOW)
        GPIO.output(stepPin, GPIO.LOW)

        time.sleep(timeDelay)

        # GPIO.OUT(stepPin, GPIO.HIGH)
        # time.sleep(timeDelay)
        # GPIO.output(STEP, GPIO.LOW)
        # time.sleep(timeDelay)

    GPIO.output(dirPin, GPIO.LOW)
    GPIO.output(stepPin, GPIO.LOW)
    GPIO.output(enablePin, GPIO.LOW)

    GPIO.cleanup()

def driveBigMotorBackward(stepPin, step):

    binaryStringStepPin = format(stepPin, '#06b')
    binaryNumArrayStepPin = list(binaryStringStepPin)

    GPIO.output(enablePin, GPIO.HIGH)

    for i in range(0, step):
        """
        Will use 1 pin for all Direction Pins, we don't really care if we set all of Forward or Backwards
        Will use 3 or 4 select pins for Step Pins and 1 other pin to choose on or off. Possibility of using 4 or 5 pins in total 
        """

        # Forward drive block
        GPIO.output(dirPin, GPIO.HIGH)
        GPIO.output(stepPin, GPIO.HIGH)

        time.sleep(timeDelay)

        GPIO.output(dirPin, GPIO.HIGH)
        GPIO.output(stepPin, GPIO.LOW)

        # GPIO.OUT(stepPin, GPIO.HIGH)
        # time.sleep(timeDelay)
        # GPIO.output(STEP, GPIO.LOW)
        # time.sleep(timeDelay)

    # Turn all of select line to 0.
    GPIO.output(dirPin, GPIO.LOW)
    GPIO.output(stepPin, GPIO.LOW)
    GPIO.output(enablePin, GPIO.LOW)

    GPIO.cleanup()
