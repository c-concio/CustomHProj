# code that moves small motors forward or backward	

import time
import RPI.GPIO as GPIO
import smbus

# ---------------------------------------------------------------
#                       Variable Changes
# variables
sleepTime = 0.01

# Driver 1
nFault1 = 16
direction1 = "forward"
address1 = 0x23
loopRange1 = 500

# Driver 2
nFault2 = 18
direction2 = "forward"
address2 = 0x24
loopRange2 = 500

# ---------------------------------------------------------------

nFaultPin1 = GPIO.setup(nFault1, GPIO.OUT, initial=GPIO.HIGH)
nFaultPin2 = GPIO.setup(nFault2, GPIO.OUT, initial=GPIO.HIGH)


bis = smbus.SMBus(1)
GPIO.setmode(GPIO.BOARD)

def driveMotor(driver):
	if drive == '1':
		nFault = nFaultPin1
		direction = direction1
		address = address1
		loopRange = loopRange1
		direction = direction1
	else:
		nFault = nFaultPin2
		direction = direction2
		address = address2
		loopRange = loopRange2
		direction = direction2

	if direction == "forward":
		for i in range(0, loopRange):
			bus.write_byte_data(address, 0x01, 0b01001100)
			time.sleep(sleepTime)

			bus.write_byte_data(address, 0x01, 0b00101100)
			time.sleep(sleepTime)

			bus.write_byte_data(address, 0x01, 0b00110100)
	    	time.sleep(sleepTime)

	    	bus.write_byte_data(address, 0x01, 0b01010100)
	    	time.sleep(sleepTime)

	    bus.write_byte_data(address, 0x01, 0b00000100)

    else:
    	for i in range(0, loopRange):
			bus.write_byte_data(address, 0x01, 0b01010100)
			time.sleep(sleepTime)

			bus.write_byte_data(address, 0x01, 0b00110100)
			time.sleep(sleepTime)

			bus.write_byte_data(address, 0x01, 0b00101100)
	    	time.sleep(sleepTime)

	    	bus.write_byte_data(address, 0x01, 0b01001100)
	    	time.sleep(sleepTime)

	    bus.write_byte_data(address, 0x01, 0b00000100)
	


# ---------------------------------------------------------------
#							Function Call

driveMotor(1)
driveMotor(2)

# ---------------------------------------------------------------

GPIO.cleanup()