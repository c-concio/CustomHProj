import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

import i2c_driver_manipulation as i2c
import BigDriver as BigDriver

# Initialization of the i2c bus.
bus = smbus.SMBus(1)

def mix():
    """
    Assume using the big motor to mix the sauce.
    """