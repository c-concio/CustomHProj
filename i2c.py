import smbus2
import time

bus = smbus2.SMBus(0)

# Default Address of each driver. Will have to set up different address for each. See 7.5.2 for the DRV8847SPWR spec sheet.
MODULE_ADDRESS = 0x60

"""
Make a for loop that takes number of calls to either (IN1 and IN2) or (IN3 and IN4) will be made.
That many calls will be the number steps the motor will be tick

REFER TO 7.6 OF THE DRV8847SPWR SPEC SHEET
HOWEVER, WILL HAVE TO TEST THE PERFORMANCE. For now, test it to see if it works. Put time delay to see ticks?
"""

