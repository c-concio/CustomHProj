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
count = 13

"""
ADDRESS 1 - 12 --> BASES: ID FROM THE DATABASE
ADDRESS 13 - 34 --> FLAVOURS: ID FROM THE DATABASE
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

AddressList = [
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
    MODULE_ADDRESS32,
    MODULE_ADDRESS33,
    MODULE_ADDRESS34
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
    # SET DISFLT TO 1 AT FIRST FOR ALL DRIVERS. Since they're all 0x60 at the beginning, it sends to all of them
    bus.write_byte_data(0x60, 0x02, 0b01000000)

    for i in range(0, AddressList.__len__()):
        # For the decoder to each activate the nfault pin on the driver. Enabling to change the address
        binaryString = format(count, '#07b')
        binaryNumArray = list(binaryString)  # Index 0 = MSB | Last Index = LSB

        """
        For the purpose of the project, we are only using 6 Bases, 6 Bases with Solenoids and 22 Flavours.
        Since we're using decoder, 00000 would talk to the first driver connected. That driver would have address 12.
        So on and so forth.
        """

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
        bus.write_byte_data(AddressList[i], 0x02, 0x00)     # SET DISFLT TO 0 AFTER EACH ADDRESS CHANGE


"""
Might need to wipe the temporary database on reboot.
"""

# connect = sqlite3.connect(r"database/pysqlite.db")
# cursor = connect.cursor()
# delete = "DELETE FROM temporary"
# cursor.execute(delete)
# cursor.close()
