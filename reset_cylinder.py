import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

import i2c_driver_manipulation as i2c
import BigDriver as BigDriver

def i2cResetCylinder(address, step):

    i2c.backwardStep(address, step)

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
    #         i2c.backwardStep(ingredient[1])
    #
    # cursor.close()

def bigResetCylinder(dirPin, stepPin, step):

    """
    :param dirPin: It's the one pin. So hardcorded pin set to either 1 (clockwise) or 0 (counter clockwise).
                    But we sending the pin number so that we can set it to HIGH or LOW.
    :param stepPin: Turn the ID from database to Binary. Then distribute to the designated pins.
    :return:
    """

    BigDriver.driveBigMotorBackward(dirPin, stepPin, step)

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
    #     if(ingredient[0] == )
