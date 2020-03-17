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
solenoidPin16 = 16
solenoidPin18 = 18
solenoidPin22 = 22
solenoidPin24 = 24
solenoidPin26 = 26
solenoidPin28 = 28
GPIO.setmode(GPIO.BOARD)  # Uses Physical pins on the Raspberry, NOT the GPIO.
GPIO.setup(solenoidPin16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(solenoidPin18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(solenoidPin22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(solenoidPin24, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(solenoidPin26, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(solenoidPin28, GPIO.OUT, initial=GPIO.LOW)

"""
GPIO Pins for the Big Motor. GOES TO DEMUX. NOT SET IN STONE YET.
"""
dirPin = 7  # direction pin

stepPin8 = 8  # step GPIO pin
stepPin10 = 10  # step GPIO pin
stepPin12 = 12  # step GPIO pin

CW = 1  # clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 287 * 200  # Steps per revolution (360 / 1.8)

GPIO.setup(dirPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepPin12, GPIO.OUT, initial=GPIO.LOW)

# #Default Address of each driver. Will have to set up different address for each. See 7.5.2 for the DRV8847SPWR spec sheet.


"""
ADDRESS (ID in Database) 1 - 12 --> BASES
ADDRESS (ID in Database) 13 - 34 --> FLAVOURS (i2c)
"""
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
MODULE_ADDRESS32 = 0x20
MODULE_ADDRESS33 = 0x21
MODULE_ADDRESS34 = 0x22

"""
REFER TO 7.6 OF THE DRV8847SPWR SPEC SHEET
HOWEVER, WILL HAVE TO TEST THE PERFORMANCE. For now, test it to see if it works. Put time delay to see ticks?
"""


def run():
    getUserData()


def pinchValveOpen(pinNumber):
    GPIO.output(pinNumber, GPIO.HIGH)

def pinchValveClose(pinNumber):
    GPIO.output(pinNumber, GPIO.LOW)

"""
Get Data from user and dispense the selections
IDs from the database starts at 1.
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
        if (combination[0] == 1):

            print("Dispense")

            # Call the driver and rotate steps to dispense.
            """
            Reason why it's 0 is because decoder. We use 4 select to 16 output demux + input for driving or not.
            For ID = 0, 0b000 will be propagated through the decoder's input and the output
            will yield the correct driver to drive. This is for the Big Motor as i2c was not
            used for it. ONLY for the step pin's select line
            """
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            BigDriver.driveBigMotorForward(dirPin, combination[0] - 1, stepCount)
            BigDriver.driveBigMotorBackward(dirPin, combination[0] - 1, 10)  # Don't know if Big Cylinder use

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
        if (combination[0] == 7):

            print("Dispense")

            # Call the driver and rotate steps to dispense.
            """
            Reason why it's 0 is because decoder. We use 4 select to 16 output demux + input for driving or not.
            For ID = 0, 0b000 will be propagated through the decoder's input and the output
            will yield the correct driver to drive. This is for the Big Motor as i2c was not
            used for it. ONLY for the step pin's select line
            """
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            pinchValveOpen(solenoidPin16)
            BigDriver.driveBigMotorForward(dirPin, combination[0] - 1, stepCount)
            BigDriver.driveBigMotorBackward(dirPin, combination[0] - 1, 10)  # Don't know if Big Cylinder use
            pinchValveClose(solenoidPin16)

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
        if (combination[0] == 13):

            print("Dispense")

            # Call the driver and rotate steps to dispense.
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            i2c.forwardStep(MODULE_ADDRESS13, stepCount)
            i2c.backwardStep(MODULE_ADDRESS13, 3)  # Because of the syringe pressure, we need to go backward to stop dispensing immediately

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
            i2c.forwardStep(MODULE_ADDRESS14, stepCount)
            i2c.backwardStep(MODULE_ADDRESS14, 3)  # Because of the syringe pressure, we need to go backward to stop dispensing immediately

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
