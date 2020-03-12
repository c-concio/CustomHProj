import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

import i2c_driver_manipulation as i2c

"""
WILL NEED TO DO THE SAME FOR THE BIG MOTOR DRIVER.
"""

def resetCylinder(address):

    connect = sqlite3.connect(r"database/pysqlite.db")
    cursor = connect.cursor()

    """
    WILL NEED A TABLE WITH MAXIMUM STEPS OF EACH CYLINDER
    """
    sqlCylinder = "SELECT id, steps from cylinder"
    cursor.execute(sqlCylinder)
    ingredientList = cursor.fetchall()

    for ingredient in ingredientList:
        if(ingredient[0] == address):
            i2c.backwardStep(ingredient[1])

    cursor.close()

