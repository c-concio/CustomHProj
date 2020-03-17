import time
import RPi.GPIO as GPIO
import i2c_initial_setup as setup

dirPin = 7  # direction pin     0: Forward  1: Backward

stepPin8 = 8  # step GPIO pin     MSB
stepPin10 = 10  # step GPIO pin
stepPin12 = 12  # step GPIO pin
stepPin32 = 32  # step GPIO pin     LSB
stepPinControl = 37  # Designated pin (1 to drive, 0 to stop drive).

CW = 1  # clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 287 * 200  # Steps per revolution (360 / 1.8)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin8, GPIO.OUT)
GPIO.setup(stepPin10, GPIO.OUT)
GPIO.setup(stepPin12, GPIO.OUT)
GPIO.setup(stepPin32, GPIO.OUT)
GPIO.setup(stepPinControl, GPIO.OUT)

timeDelay = 0.01

"""
Work in term of the decoder
stepPin also means which ID of the cylinder.
"""

def driveBigMotorForward(stepPin, step):
    binaryStringStepPin = format(stepPin, '#06b')
    binaryNumArrayStepPin = list(binaryStringStepPin)

    # Select line that goes through the select lines from the DEMUX to select correct driver.
    GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)     # Makes sure that it doesn't run at the beginning.
    setup.GPIO_High_Low(stepPin8, int(binaryNumArrayStepPin[0]))
    setup.GPIO_High_Low(stepPin10, int(binaryNumArrayStepPin[1]))
    setup.GPIO_High_Low(stepPin12, int(binaryNumArrayStepPin[2]))
    setup.GPIO_High_Low(stepPin32, int(binaryNumArrayStepPin[3]))

    for i in range(0, step):

        """
        Will use 1 pin for all Direction Pins, we don't really care if we set all of Forward or Backwards
        Will use 3 or 4 select pins for Step Pins and 1 other pin to choose on or off. Possibility of using 4 or 5 pins in total 
        """

        # Forward drive block
        GPIO.output(dirPin, GPIO.OUT, GPIO.LOW)
        GPIO.output(stepPinControl, GPIO.OUT, GPIO.HIGH)

        time.sleep(timeDelay)

        GPIO.output(dirPin, GPIO.OUT, GPIO.LOW)
        GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)

        time.sleep(timeDelay)

        # GPIO.OUT(stepPin, GPIO.HIGH)
        # time.sleep(timeDelay)
        # GPIO.output(STEP, GPIO.LOW)
        # time.sleep(timeDelay)

    # Turn all of select line to 0.
    GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)
    GPIO.output(dirPin, GPIO.OUT, GPIO.LOW)
    GPIO.output(stepPin8, GPIO.OUT, GPIO.LOW)
    GPIO.output(stepPin10, GPIO.OUT, GPIO.LOW)
    GPIO.output(stepPin12, GPIO.OUT, GPIO.LOW)

    GPIO.cleanup()

def driveBigMotorBackward(stepPin, step):

    binaryStringStepPin = format(stepPin, '#06b')
    binaryNumArrayStepPin = list(binaryStringStepPin)

    # Select line that goes through the select lines from the DEMUX to select correct driver.
    GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)  # Makes sure that it doesn't run at the beginning.
    setup.GPIO_High_Low(stepPin8, int(binaryNumArrayStepPin[0]))
    setup.GPIO_High_Low(stepPin10, int(binaryNumArrayStepPin[1]))
    setup.GPIO_High_Low(stepPin12, int(binaryNumArrayStepPin[2]))
    setup.GPIO_High_Low(stepPin32, int(binaryNumArrayStepPin[3]))

    for i in range(0, step):
        """
        Will use 1 pin for all Direction Pins, we don't really care if we set all of Forward or Backwards
        Will use 3 or 4 select pins for Step Pins and 1 other pin to choose on or off. Possibility of using 4 or 5 pins in total 
        """

        # Forward drive block
        GPIO.output(dirPin, GPIO.OUT, GPIO.HIGH)
        GPIO.output(stepPinControl, GPIO.OUT, GPIO.HIGH)

        time.sleep(timeDelay)

        GPIO.output(dirPin, GPIO.OUT, GPIO.HIGH)
        GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)

        # GPIO.OUT(stepPin, GPIO.HIGH)
        # time.sleep(timeDelay)
        # GPIO.output(STEP, GPIO.LOW)
        # time.sleep(timeDelay)

    # Turn all of select line to 0.
    GPIO.output(stepPinControl, GPIO.OUT, GPIO.LOW)
    GPIO.output(dirPin, GPIO.OUT, GPIO.LOW)
    GPIO.output(stepPin8, GPIO.OUT, GPIO.LOW)
    GPIO.output(stepPin10, GPIO.OUT, GPIO.LOW)
    GPIO.output(stepPin12, GPIO.OUT, GPIO.LOW)

    GPIO.cleanup()
