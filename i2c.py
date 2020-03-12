import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

import i2c_driver_manipulation as i2c
import BigDriver as BigDriver

# Initialization of the i2c bus.
bus = smbus.SMBus(1)

"""
GPIO ON THE PI TO CONTROL THE SOLENOIDS' PINCH VALVES
NOT WHICH PINS IS YET TO BE SET
"""
GPIO.setmode(GPIO.BOARD)  # Uses Physical pins on the Raspberry, NOT the GPIO.
GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)

"""
GPIO Pins for the Big Motor. GOES TO DECODER. NOT SET IN STONE YET.
"""
dirPin8 = 8  # direction pin
stepPin11 = 11  # step GPIO pin

dirPin10 = 10  # direction pin
stepPin13 = 13  # step GPIO pin

dirPin12 = 12  # direction pin
stepPin15 = 15  # step GPIO pin

CW = 1  # clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 287 * 200  # Steps per revolution (360 / 1.8)

# #Default Address of each driver. Will have to set up different address for each. See 7.5.2 for the DRV8847SPWR spec sheet.


"""
ADDRESS 0 - 9 --> BASES
ADDRESS 10+ --> FLAVOURS
"""
MODULE_ADDRESS0 = 0x00
MODULE_ADDRESS1 = 0x01
MODULE_ADDRESS2 = 0x02
MODULE_ADDRESS3 = 0x03
MODULE_ADDRESS4 = 0x04
MODULE_ADDRESS5 = 0x05
MODULE_ADDRESS6 = 0x06
MODULE_ADDRESS7 = 0x07
MODULE_ADDRESS8 = 0x08
MODULE_ADDRESS9 = 0x09
MODULE_ADDRESS10 = 0x0A
MODULE_ADDRESS11 = 0x0B
MODULE_ADDRESS12 = 0x0C
MODULE_ADDRESS13 = 0x0D
MODULE_ADDRESS14 = 0x0E
MODULE_ADDRESS15 = 0x0F
MODULE_ADDRESS16 = 0x10
MODULE_ADDRESS17 = 0x11
MODULE_ADDRESS18 = 0x12
MODULE_ADDRESS19 = 0x13
MODULE_ADDRESS20 = 0x14
MODULE_ADDRESS21 = 0x15
MODULE_ADDRESS22 = 0x16
MODULE_ADDRESS23 = 0x17
MODULE_ADDRESS24 = 0x18
MODULE_ADDRESS25 = 0x19
MODULE_ADDRESS26 = 0x1A
MODULE_ADDRESS27 = 0x1B
MODULE_ADDRESS28 = 0x1C
MODULE_ADDRESS29 = 0x1D
MODULE_ADDRESS30 = 0x1E
MODULE_ADDRESS31 = 0x1F

"""
Make a for loop that takes number of calls to either (IN1 and IN2) or (IN3 and IN4) will be made.
That many calls will be the number steps the motor will be tick (HAVE TO TEST IT OUT, WE STILL HAVENT FIXED THE CIRCUIT)
#
REFER TO 7.6 OF THE DRV8847SPWR SPEC SHEET
HOWEVER, WILL HAVE TO TEST THE PERFORMANCE. For now, test it to see if it works. Put time delay to see ticks?
"""


def run():
    getUserData()


def pinchValveDispense(pinNumber, theTime):
    GPIO.setmode(GPIO.BOARD)  # Uses the physical pin number from the Rapsberry Pi. NO THE GPIO number
    GPIO.setup(pinNumber, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(pinNumber, True)
    time.sleep(theTime)
    GPIO.output(pinNumber, False)


"""
Get Data from user and dispense the selections
"""


def getUserData():
    connect = sqlite3.connect(r"database/pysqlite.db")
    cursor = connect.cursor()

    sqlTemp = "SELECT cylinder_id, ml FROM temporary"
    cursor.execute(sqlTemp)
    userInputs = cursor.fetchall()
    # print(userInputs[0][1])

    sqlCylinder = "SELECT id, steps from cylinder"
    cursor.execute(sqlCylinder)
    updateStepsList = cursor.fetchall()
    # print(updateStepsList)

    for combination in userInputs:
        print(combination)
        print(combination[0])
        """
        Go in the local database in temporary and extract all the stuff.
        Once extracted, correspond the ID to the driver address.
        The ifs are acting like a Switch statement. So will have to
        associate for each available ID and the subsequent code.
        IMPORTANT: Each ID will have different time for the solenoid valve
        to be open because of their consistency.
        """

        # If ID corresponds to the one at current combination.
        if (combination[0] == 0):

            print("Dispense")

            # Call the driver and rotate steps to dispense.
            """
            Reason why it's 0 is because decoder. We use 3 input to 8 output decoder.
            For ID = 0, 0b000 will be propagated through the decoder's input and the output
            will yield the correct driver to drive. This is for the Big Motor as i2c was not
            used for it.
            """
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            BigDriver.driveBigMotor(0, 0, CW, stepCount)
            BigDriver.driveBigMotor(0, 0, CCW, 10)  # Don't know if Big Cylinder use

            """
            ADD IN CODE FOR GPIO to open and close Pinch valves to dispense
            ONLY FOR THE ONES THAT USES GRAVITY
            """
            pinchValveDispense(20, 2)

            """
            UPDATING THE DATABASE AFTER DISPENSING
            """
            newValue = 0
            for entry in updateStepsList:
                # print(entry)
                # Updating the database in the total amount of the
                if (entry[0] == combination[0]):
                    print(entry[0])
                    print(entry[1])
                    oldValue = entry[1]
                    newValue = oldValue + combination[1]
                    break

            sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
            data = (newValue, combination[0])
            cursor.execute(sqlCylinderNew, data)
            connect.commit()

        # If ID corresponds to the one at current combination.
        if (combination[0] == 10):

            print("Dispense")

            # Call the driver and rotate steps to dispense.
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            i2c.forwardStep(MODULE_ADDRESS1, stepCount)
            i2c.backwardStep(MODULE_ADDRESS1,
                             3)  # Because of the syringe pressure, we need to go backward to stop dispensing immediately

            """
            ADD IN CODE FOR GPIO to open and close Pinch valves to dispense
            ONLY FOR THE ONES THAT USES GRAVITY
            """
            pinchValveDispense(15, 2)

            """
            UPDATING THE DATABASE AFTER DISPENSING
            """
            newValue = 0
            for entry in updateStepsList:
                # print(entry)
                if (entry[0] == combination[0]):
                    print(entry[0])
                    print(entry[1])
                    oldValue = entry[1]
                    newValue = oldValue + combination[1]
                    break

            sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
            data = (newValue, combination[0])
            cursor.execute(sqlCylinderNew, data)
            connect.commit()

        # If ID corresponds to the one at current combination.
        if (combination[0] == 14):

            print("Dispense")

            # Call the driver and rotate steps to dispense.
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            i2c.forwardStep(MODULE_ADDRESS4, stepCount)
            i2c.backwardStep(MODULE_ADDRESS4,
                             3)  # Because of the syringe pressure, we need to go backward to stop dispensing immediately

            """
            ADD IN CODE FOR GPIO to open and close Pinch valves to dispense
            ONLY FOR THE ONES THAT USES GRAVITY
            """
            pinchValveDispense(15, 2)

            """
            UPDATING THE DATABASE AFTER DISPENSING
            """
            newValue = 0
            for entry in updateStepsList:
                # print(entry)
                # Updating the database in the total amount of the
                if (entry[0] == combination[0]):
                    print(entry[0])
                    print(entry[1])
                    oldValue = entry[1]
                    newValue = oldValue + combination[1]
                    break

            sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
            data = (newValue, combination[0])
            cursor.execute(sqlCylinderNew, data)
            connect.commit()

    """
    At the end, delete all entries in the TEMPORARY.
    Something along the line of sql = 'DELETE FROM tasks'.
    Then Cursor.Close()
    """
    # delete = "DELETE FROM temporary"
    # cursor.execute(delete)
    cursor.close()


"""
Mixing of the ingredients.
"""

run()
