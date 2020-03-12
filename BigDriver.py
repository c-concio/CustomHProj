import time
import RPi.GPIO as GPIO
import i2c_initial_setup as setup

dirPin8 = 8  # direction pin
stepPin11 = 11  # step GPIO pin

dirPin10 = 10  # direction pin
stepPin13 = 13  # step GPIO pin

dirPin12 = 12  # direction pin
stepPin15 = 15  # step GPIO pin

CW = 1  # clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 287 * 200  # Steps per revolution (360 / 1.8)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(dirPin8, GPIO.OUT)
GPIO.setup(stepPin11, GPIO.OUT)

GPIO.setup(dirPin10, GPIO.OUT)
GPIO.setup(stepPin13, GPIO.OUT)

GPIO.setup(dirPin12, GPIO.OUT)
GPIO.setup(stepPin15, GPIO.OUT)

timeDelay = 0.01

"""
Work in term of the decoder
"""

def driveBigMotor(directionPin, stepPin, direction, step):

    binaryStringDirectionPin = format(directionPin, '#05b')
    binaryStringStepPin = format(stepPin, '#05b')

    binaryNumArrayDirectionPin = list(binaryStringDirectionPin)
    binaryNumArrayStepPin = list(binaryStringStepPin)

    # GPIO.output(directionPin, direction)

    for i in range(0, step):

        """
        How to send the direction (Clockwise = 1, CCW = 0) through the decoder?
        WILL NEED TO INVESTIGATE
        """

        # Sends combination of signals to decoder to activate at which driver.
        setup.GPIO_High_Low(dirPin8, int(binaryNumArrayDirectionPin[0]))
        setup.GPIO_High_Low(stepPin11, int(binaryNumArrayStepPin[0]))

        setup.GPIO_High_Low(dirPin10, int(binaryNumArrayDirectionPin[0]))
        setup.GPIO_High_Low(stepPin13, int(binaryNumArrayStepPin[0]))

        setup.GPIO_High_Low(dirPin12, int(binaryNumArrayDirectionPin[0]))
        setup.GPIO_High_Low(stepPin15, int(binaryNumArrayStepPin[0]))

        time.sleep(timeDelay)

        GPIO.output(dirPin8, GPIO.OUT, GPIO.LOW)
        GPIO.output(stepPin11, GPIO.OUT, GPIO.LOW)

        GPIO.output(dirPin10, GPIO.OUT, GPIO.LOW)
        GPIO.output(stepPin13, GPIO.OUT, GPIO.LOW)

        GPIO.output(dirPin12, GPIO.OUT, GPIO.LOW)
        GPIO.output(stepPin15, GPIO.OUT, GPIO.LOW)

        # GPIO.OUT(stepPin, GPIO.HIGH)
        # time.sleep(timeDelay)
        # GPIO.output(STEP, GPIO.LOW)
        # time.sleep(timeDelay)


GPIO.cleanup()
