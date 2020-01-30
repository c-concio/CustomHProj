# import smbus2
import time
import sqlite3

# bus = smbus2.SMBus(1)
#
# #Default Address of each driver. Will have to set up different address for each. See 7.5.2 for the DRV8847SPWR spec sheet.

"""
Hardcode the IDs that will be related to the driver's address.
"""
# MODULE_ADDRESS1 = 0x60
#MODULE_ADDRESS2 = 0x02
#MODULE_ADDRESS3 = 0x03
#MODULE_ADDRESS4 = 0x04
#MODULE_ADDRESS5 = 0x05
#MODULE_ADDRESS6 = 0x06

"""
Make a for loop that takes number of calls to either (IN1 and IN2) or (IN3 and IN4) will be made.
That many calls will be the number steps the motor will be tick

REFER TO 7.6 OF THE DRV8847SPWR SPEC SHEET
HOWEVER, WILL HAVE TO TEST THE PERFORMANCE. For now, test it to see if it works. Put time delay to see ticks?
"""



def run():
    getUserData()


def getUserData():
    connect = sqlite3.connect(r"database\pysqlite.db")
    cursor = connect.cursor()

    sqlTemp = "SELECT cylinder_id, ml FROM temporary"
    cursor.execute(sqlTemp)
    userInputs = cursor.fetchall()
    #print(userInputs[0][1])

    sqlCylinder = "SELECT id, steps from cylinder"
    cursor.execute(sqlCylinder)
    updateStepsList = cursor.fetchall()
    print(updateStepsList)

    for combination in userInputs:
        print(combination)
        print(combination[0])
        """
        Go in the local database in temporary and extract all the stuff.
        Once extracted, correspond the ID to the driver address.
        """
        if(combination[0] == 1):
            for count1 in range(combination[1]):
                print(combination[1])
                """
                WE DON'T KNOW IF EACH TICK WOULD BE EVERYTIME WE ENTER THE FOR LOOP
                OR THE FOR LOOP DOES NOT MATTER.
                """
                #bus.write_byte_data(MODULE_ADDRESS1, 0x01, 0b00001100)

                """
                Updating database after dispensing the content.
                """

            newValue = 0
            for entry in updateStepsList:
                print(entry)
                if (entry[0] == combination[0]):
                    print(entry[0])
                    oldValue = entry[0]
                    newValue = oldValue - combination[1]

            sqlCylinderNew = "UPDATE cylinder SET steps = ? WHERE id = ?"
            data = (newValue, combination[0])
            cursor.execute(sqlCylinderNew, data)
            connect.commit()
            #cursor.close()


        if(combination[0] == "2"):
            for count in range(combination[1]):
                for count2 in range(combination[1]):
                    """
                    WE DON'T KNOW IF EACH TICK WOULD BE EVERYTIME WE ENTER THE FOR LOOP
                    OR THE FOR LOOP DOES NOT MATTER.
                    """
                    # bus.write_byte_data(MODULE_ADDRESS1, 0x01, 0b00001100)

                    """
                    Updating database after dispensing the content.
                    """




run()
