import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

# Initialization of the i2c bus.
bus = smbus.SMBus(1)

"""
ADDRESS 1 - 12 --> BASES
ADDRESS 13+ --> FLAVOURS
"""
# MODULE_ADDRESS13 = 0x0D
# MODULE_ADDRESS14 = 0x0E
# MODULE_ADDRESS15 = 0x0F
# MODULE_ADDRESS16 = 0x10
# MODULE_ADDRESS17 = 0x11
# MODULE_ADDRESS18 = 0x12
# MODULE_ADDRESS19 = 0x13
# MODULE_ADDRESS20 = 0x14
# MODULE_ADDRESS21 = 0x15
# MODULE_ADDRESS22 = 0x16
# MODULE_ADDRESS23 = 0x17
# MODULE_ADDRESS24 = 0x18
# MODULE_ADDRESS25 = 0x19
# MODULE_ADDRESS26 = 0x1A
# MODULE_ADDRESS27 = 0x1B
# MODULE_ADDRESS28 = 0x1C
# MODULE_ADDRESS29 = 0x1D
# MODULE_ADDRESS30 = 0x1E
# MODULE_ADDRESS31 = 0x1F
# MODULE_ADDRESS32 = 0x20
# MODULE_ADDRESS33 = 0x21
# MODULE_ADDRESS34 = 0x22

"""
1 FOR LOOP = 4 TICKS ON THE DRIVER
"""

timeDelay = 0.01

def forwardStep(address, step):
    for i in range(0, step):
        # Driving forward
        # 1 & 3 high
        bus.write_byte_data(address, 0x01, 0b00101100)
        time.sleep(timeDelay)
        print("1 & 3 high")
        # 2 & 3 high
        bus.write_byte_data(address, 0x01, 0b00110100)
        time.sleep(timeDelay)
        print("2 & 3 high")
        # 2 & 4 high
        bus.write_byte_data(address, 0x01, 0b01010100)
        time.sleep(timeDelay)
        print("2 & 4 high")
        # 1 & 4 high
        bus.write_byte_data(address, 0x01, 0b01001100)
        time.sleep(timeDelay)
        print("1 & 4 high")

    bus.write_byte_data(address, 0x01, 0b00000100)

def backwardStep(address, step):
    for i in range(0, step):
        # 1 & 4 high
        bus.write_byte_data(address, 0x01, 0b01001100)
        time.sleep(timeDelay)
        print("1 & 4 high")
        # 2 & 4 high
        bus.write_byte_data(address, 0x01, 0b01010100)
        time.sleep(timeDelay)
        print("2 & 4 high")
        # 2 & 3 high
        bus.write_byte_data(address, 0x01, 0b00110100)
        time.sleep(timeDelay)
        print("2 & 3 high")
        # 1 & 3 high
        bus.write_byte_data(address, 0x01, 0b00101100)
        time.sleep(timeDelay)
        print("1 & 3 high")

    bus.write_byte_data(address, 0x01, 0b00000100)