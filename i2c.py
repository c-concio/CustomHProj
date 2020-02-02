# import smbus2
import time
import sqlite3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # Uses Physical pins on the Raspberry, NOT the GPIO.
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)


def activateGPIO(theTime, pin):
    print("LED CALLED " + str(theTime) + " " + str(pin))
    count = 0
    while (count < theTime):
        GPIO.output(pin, True)
        time.sleep(0.1)
        GPIO.output(pin, False)
        time.sleep(0.1)
        count += 1


# bus = smbus2.SMBus(1)
#
# #Default Address of each driver. Will have to set up different address for each. See 7.5.2 for the DRV8847SPWR spec sheet.

"""
Hardcode the IDs that will be related to the driver's address.
"""
MODULE_ADDRESS1 = 0x60
# MODULE_ADDRESS2 = 0x02
# MODULE_ADDRESS3 = 0x03
# MODULE_ADDRESS4 = 0x04
# MODULE_ADDRESS5 = 0x05
# MODULE_ADDRESS6 = 0x06

"""
Make a for loop that takes number of calls to either (IN1 and IN2) or (IN3 and IN4) will be made.
That many calls will be the number steps the motor will be tick

REFER TO 7.6 OF THE DRV8847SPWR SPEC SHEET
HOWEVER, WILL HAVE TO TEST THE PERFORMANCE. For now, test it to see if it works. Put time delay to see ticks?
"""

flagEmpty = False


def run():
    getUserData()

    if (flagEmpty == True):
        """
        Light up LED.
        """
        print("Empty")


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
        """
        # If ID corresponds to the one at current combination.
        if (combination[0] == 1):
            for count1 in range(combination[1]):
                # print(combination[1])
                """
                WE DON'T KNOW IF EACH TICK WOULD BE EVERYTIME WE ENTER THE FOR LOOP
                OR THE FOR LOOP DOES NOT MATTER.
                """
                #bus.write_byte_data(MODULE_ADDRESS1, 0x01, 0b00001100)

                print("Dispense")
                activateGPIO(5, 15)

                """
                Updating database after dispensing the content.
                """

            """
            ADD IN GPIO TO LIGHT THE LED HERE CODE HERE.
            Blink 5 Times to signify dispense
            """

            newValue = 0
            for entry in updateStepsList:
                # print(entry)
                if (entry[0] == combination[0]):
                    print(entry[0])
                    print(entry[1])
                    oldValue = entry[1]
                    newValue = oldValue - combination[1]
                    break

            sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
            data = (newValue, combination[0])
            cursor.execute(sqlCylinderNew, data)
            connect.commit()
            cursor.close()

            # If the total value is smaller than a certain threshold, breaks the for loop. Stop the whole process. Light up LED.
            if (newValue < 10):
                listOfGlobal = globals()
                listOfGlobal['flagEmpty'] = True
                break

            print("Update values in Database")
            activateGPIO(3, 15)
            """
            ADD GPIO BLINK LIGHT HERE -> 3x to update database.
            """

        if (combination[0] == 4):
            for count1 in range(combination[1]):
                # print(combination[1])
                """
                WE DON'T KNOW IF EACH TICK WOULD BE EVERYTIME WE ENTER THE FOR LOOP
                OR THE FOR LOOP DOES NOT MATTER.
                """
                # bus.write_byte_data(MODULE_ADDRESS1, 0x01, 0b00001100)

                print("Dispense")
                activateGPIO(5, 16)

                """
                Updating database after dispensing the content.
                """

            """
            ADD IN GPIO TO LIGHT THE LED HERE CODE HERE.
            Blink 5 Times to signify dispense
            """

            newValue = 0
            for entry in updateStepsList:
                # print(entry)
                if (entry[0] == combination[0]):
                    print(entry[0])
                    print(entry[1])
                    oldValue = entry[1]
                    newValue = oldValue - combination[1]
                    break

            sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
            data = (newValue, combination[0])
            cursor.execute(sqlCylinderNew, data)
            connect.commit()
            cursor.close()

            # If the total value is smaller than a certain threshold, breaks the for loop. Stop the whole process. Light up LED.
            if (newValue < 10):
                listOfGlobal = globals()
                listOfGlobal['flagEmpty'] = True
                break

            print("Update values in Database")
            activateGPIO(3, 16)
            """
            ADD GPIO BLINK LIGHT HERE -> 3x to update database.
            """

    """
    At the end, delete all entries in the TEMPORARY. 
    Something along the line of sql = 'DELETE FROM tasks'.
    Then Cursor.Close() 

    ADD GPIO Turning LED up to end the whole dispensing process.
    """


"""
Reset the Cylinders whenever the bag is changed OR when it reaches 0.
"""

"""
Control the relay?
Turning GPIO ON/OFF on the attached relay. Again, hardcode the which GPIO with which Relay.
"""

run()
