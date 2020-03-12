import time
import sqlite3
import RPi.GPIO as GPIO
import smbus

GPIO.setmode(GPIO.BOARD)  # Uses Physical pins on the Raspberry, NOT the GPIO.
# NEED TO SET UP PINS FOR EACH NFAULT OF EACH DRIVER. USE DEMUX OR DECODER FOR THAT
PIN27 = 27  # MSB
PIN29 = 29
PIN31 = 31
PIN33 = 33
PIN35 = 35  # LSB

GPIO.setup(PIN27, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN29, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN31, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN33, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN35, GPIO.OUT, initial=GPIO.LOW)

bus = smbus.SMBus(1)
count = 0

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

AddressList = [
    MODULE_ADDRESS0,
    MODULE_ADDRESS1,
    MODULE_ADDRESS2,
    MODULE_ADDRESS3,
    MODULE_ADDRESS4,
    MODULE_ADDRESS5,
    MODULE_ADDRESS6,
    MODULE_ADDRESS7,
    MODULE_ADDRESS8,
    MODULE_ADDRESS9,
    MODULE_ADDRESS10,
    MODULE_ADDRESS11,
    MODULE_ADDRESS12,
    MODULE_ADDRESS13,
    MODULE_ADDRESS14,
    MODULE_ADDRESS15,
    MODULE_ADDRESS16,
    MODULE_ADDRESS17,
    MODULE_ADDRESS18,
    MODULE_ADDRESS19,
    MODULE_ADDRESS20,
    MODULE_ADDRESS21,
    MODULE_ADDRESS22,
    MODULE_ADDRESS23,
    MODULE_ADDRESS24,
    MODULE_ADDRESS25,
    MODULE_ADDRESS26,
    MODULE_ADDRESS27,
    MODULE_ADDRESS28,
    MODULE_ADDRESS29,
    MODULE_ADDRESS30,
    MODULE_ADDRESS31,
]


def GPIO_High_Low(pinNumber, binary):
    if (binary == 1):
        GPIO.output(pinNumber, GPIO.OUT, GPIO.HIGH)
    else:
        GPIO.output(pinNumber, GPIO.OUT, GPIO.LOW)

def addressInit():
    """
    Resetting default address of each driver to their corresponding address.
    DEFAULT SET TO 32 DRIVERS FOR 32 MOTORS.
    """
    for i in range(0, AddressList.__len__()):
        # For the decoder to each activate the nfault pin on the driver. Enabling to change the address
        binaryString = format(count, '#07b')
        binaryNumArray = list(binaryString)  # Index 0 = MSB | Last Index = LSB

        """
        For the purpose of the project, we are only using 6 Bases and 22 Flavours.
        Therefore, we're omitting addresses 6 to 9.
        """
        if (i == 6 or i == 7 or i == 8 or i == 9):
            continue

        GPIO_High_Low(PIN27, int(binaryNumArray[0]))
        GPIO_High_Low(PIN29, int(binaryNumArray[1]))
        GPIO_High_Low(PIN31, int(binaryNumArray[2]))
        GPIO_High_Low(PIN33, int(binaryNumArray[3]))
        GPIO_High_Low(PIN35, int(binaryNumArray[4]))

        # GPIO.output(PIN27, GPIO.OUT, int(binaryNumArray[0]))
        # GPIO.output(PIN29, GPIO.OUT, int(binaryNumArray[1]))
        # GPIO.output(PIN31, GPIO.OUT, int(binaryNumArray[2]))
        # GPIO.output(PIN33, GPIO.OUT, int(binaryNumArray[3]))
        # GPIO.output(PIN35, GPIO.OUT, int(binaryNumArray[4]))

        time.sleep(0.01)
        # Writing address for designated driver numbers.
        bus.write_byte_data(0x60, 0x00, AddressList[i])


"""
Might need to wipe the temporary database on reboot.
"""

# connect = sqlite3.connect(r"database/pysqlite.db")
# cursor = connect.cursor()
# delete = "DELETE FROM temporary"
# cursor.execute(delete)
# cursor.close()
