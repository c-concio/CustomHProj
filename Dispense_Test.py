import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

import i2c_driver_manipulation as i2c
import BigDriver as BigDriver

# Initialization of the i2c bus.
bus = smbus.SMBus(1)

dir1 = 11
dir2 = 19

stepPin1 = 13
stepPin2 = 21

solenoidPin16 = 16
solenoidPin18 = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(dir1, GPIO.OUT)
GPIO.setup(dir2, GPIO.OUT)
GPIO.setup(stepPin1, GPIO.OUT)
GPIO.setup(stepPin2, GPIO.OUT)
GPIO.setup(solenoidPin16, GPIO.OUT)
GPIO.setup(solenoidPin18, GPIO.OUT)

def Test():
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
            # Forward
            stepCount = combination[1]  # CHECK IF THIS GETS THE SAVED AMOUNT IN THE DATABASE
            for i in range(0, stepCount):
                GPIO.output(dir1, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin1, GPIO.OUT, GPIO.HIGH)

                time.sleep(0.01)

                GPIO.output(dir1, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin1, GPIO.OUT, GPIO.LOW)

                time.sleep(0.01)
            GPIO.cleanup()

            # Backward
            for i in range(0, 5):
                GPIO.output(dir2, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin2, GPIO.OUT, GPIO.HIGH)

                time.sleep(0.01)

                GPIO.output(dir2, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin2, GPIO.OUT, GPIO.LOW)

                time.sleep(0.01)
            GPIO.cleanup()

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

            GPIO.output(solenoidPin16, GPIO.OUT, GPIO.HIGH)

            # Forward
            for i in range(0, stepCount):
                GPIO.output(dir1, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin1, GPIO.OUT, GPIO.HIGH)

                time.sleep(0.01)

                GPIO.output(dir1, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin1, GPIO.OUT, GPIO.LOW)

                time.sleep(0.01)
            GPIO.cleanup()

            # Backward
            for i in range(0, 5):
                GPIO.output(dir2, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin2, GPIO.OUT, GPIO.HIGH)

                time.sleep(0.01)

                GPIO.output(dir2, GPIO.OUT, GPIO.LOW)
                GPIO.output(stepPin2, GPIO.OUT, GPIO.LOW)

                time.sleep(0.01)
            GPIO.cleanup()

            GPIO.output(solenoidPin16, GPIO.OUT, GPIO.LOW)

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

            for i in range(0, stepCount):
                # Driving forward
                # 1 & 3 high
                bus.write_byte_data(0x23, 0x01, 0b00101100)
                time.sleep(0.01)
                print("1 & 3 high")
                # 2 & 3 high
                bus.write_byte_data(0x23, 0x01, 0b00110100)
                time.sleep(0.01)
                print("2 & 3 high")
                # 2 & 4 high
                bus.write_byte_data(0x23, 0x01, 0b01010100)
                time.sleep(0.01)
                print("2 & 4 high")
                # 1 & 4 high
                bus.write_byte_data(0x23, 0x01, 0b01001100)
                time.sleep(0.01)
                print("1 & 4 high")

            bus.write_byte_data(0x23, 0x01, 0b00000100)

            for i in range(0, stepCount):
                # 1 & 4 high
                bus.write_byte_data(0x23, 0x01, 0b01001100)
                time.sleep(0.01)
                print("1 & 4 high")
                # 2 & 4 high
                bus.write_byte_data(0x23, 0x01, 0b01010100)
                time.sleep(0.01)
                print("2 & 4 high")
                # 2 & 3 high
                bus.write_byte_data(0x23, 0x01, 0b00110100)
                time.sleep(0.01)
                print("2 & 3 high")
                # 1 & 3 high
                bus.write_byte_data(0x23, 0x01, 0b00101100)
                time.sleep(0.01)
                print("1 & 3 high")

            bus.write_byte_data(0x23, 0x01, 0b00000100)
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

            for i in range(0, stepCount):
                # Driving forward
                # 1 & 3 high
                bus.write_byte_data(0x24, 0x01, 0b00101100)
                time.sleep(0.01)
                print("1 & 3 high")
                # 2 & 3 high
                bus.write_byte_data(0x24, 0x01, 0b00110100)
                time.sleep(0.01)
                print("2 & 3 high")
                # 2 & 4 high
                bus.write_byte_data(0x24, 0x01, 0b01010100)
                time.sleep(0.01)
                print("2 & 4 high")
                # 1 & 4 high
                bus.write_byte_data(0x24, 0x01, 0b01001100)
                time.sleep(0.01)
                print("1 & 4 high")

            bus.write_byte_data(0x24, 0x01, 0b00000100)

            for i in range(0, stepCount):
                # 1 & 4 high
                bus.write_byte_data(0x23, 0x01, 0b01001100)
                time.sleep(0.01)
                print("1 & 4 high")
                # 2 & 4 high
                bus.write_byte_data(0x23, 0x01, 0b01010100)
                time.sleep(0.01)
                print("2 & 4 high")
                # 2 & 3 high
                bus.write_byte_data(0x23, 0x01, 0b00110100)
                time.sleep(0.01)
                print("2 & 3 high")
                # 1 & 3 high
                bus.write_byte_data(0x23, 0x01, 0b00101100)
                time.sleep(0.01)
                print("1 & 3 high")

            bus.write_byte_data(0x23, 0x01, 0b00000100)
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