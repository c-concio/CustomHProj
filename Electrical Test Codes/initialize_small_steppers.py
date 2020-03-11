import time
import RPI.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)
GPIO.setmode(GPIO.BOARD)

# ---------------------------------------------------------------
#                       Variable Changes

# Driver 1
nFault1 = 16
newAddress1 = 0x23

# Driver 2
nFault2 = 18
newAddress2 = 0x24

# ---------------------------------------------------------------

nFaultPin1 = GPIO.setup(nFault1, GPIO.OUT, initial=GPIO.HIGH)
nFaultPin2 = GPIO.setup(nFault2, GPIO.OUT, initial=GPIO.HIGH)

bus.write_byte_data(0x60, 0x02, 0b01000000)

GPIO.output(16, True)
GPIO.output(18, False)
bus.write_byte_data(0x60, 0x00, newAddress1)
time.sleep(1)
bus.write_byte_data(newAddress1, 0x02, 0x00)
time.sleep(1)

GPIO.output(16, False)
GPIO.output(18, True)
bus.write_byte_data(0x60, 0x00, newAddress2)
time.sleep(1)
bus.write_byte_data(newAddress2, 0x02, 0x00)
GPIO.output(18, False)

GPIO.cleanup()