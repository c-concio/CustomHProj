import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

import i2c_driver_manipulation as i2c
import BigDriver as BigDriver

def i2cResetCylinder(address, step):

    i2c.backwardStep(address, step)

    # """
    # Steps to be fed in. better to update database on hardware side.
    # Will do (steps fed - remaining amount). Then backward this steps.
    # """
    #
    # connect = sqlite3.connect(r"database/pysqlite.db")
    # cursor = connect.cursor()
    #
    # """
    # Software will feed in the address (ID from the database) and the steps.
    # """
    # sqlCylinder = "SELECT id, steps from cylinder"
    # cursor.execute(sqlCylinder)
    # ingredientList = cursor.fetchall()
    #
    # for ingredient in ingredientList:
    #     if(ingredient[0] == address):
    #         total = step - ingredient[1]
    #         i2c.backwardStep(address, total)
    #
    #         sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
    #         data = (step, ingredient[0])
    #         cursor.execute(sqlCylinderNew, data)
    #         cursor.commit()
    #
    # cursor.close()

def bigResetCylinder(stepPin, step):

    """
    :param dirPin: It's the one pin. So hardcorded pin set to either 1 (clockwise) or 0 (counter clockwise).
                    But we sending the pin number so that we can set it to HIGH or LOW.
    :param stepPin: Turn the ID from database to Binary. Then distribute to the designated pins.
    :return:
    """

    BigDriver.driveBigMotorBackward(stepPin, step)

    # connect = sqlite3.connect(r"database/pysqlite.db")
    # cursor = connect.cursor()
    #
    # """
    # WILL NEED A TABLE WITH MAXIMUM STEPS OF EACH CYLINDER
    # """
    # sqlCylinder = "SELECT id, steps from cylinder"
    # cursor.execute(sqlCylinder)
    # ingredientList = cursor.fetchall()
    #
    # for ingredient in ingredientList:
    #     if(ingredient[0] == stepPin):
    #         total = step - ingredient[1]
    #         BigDriver.driveBigMotorForward(stepPin, total)
    #
    #         sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
    #         data = (step, ingredient[0])
    #         cursor.execute(sqlCylinderNew, data)
    #         cursor.commit()
    #
    # cursor.close()
