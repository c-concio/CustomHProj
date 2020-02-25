import kivy
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase

import i2c
from Model import UserModel, DatabaseClass, MainModel

kivy.require('1.9.0')


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'left'
    MainModel.mainScreenManager.current = screen_name
    return


# def return_screen(screen_name):
#     UserModel.screenManager.transition.direction = 'right'
#     UserModel.screenManager.current = screen_name


# Button switches to
def initialize_buttons():
    # Step buttons
    UserModel.splitScreen.step1.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.sizeScreen))
    UserModel.splitScreen.step2.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.step3.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.step4.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))

    UserModel.splitScreen.step1.bind(on_press=lambda x: deleteAmountScreen())
    UserModel.splitScreen.step2.bind(on_press=lambda x: deleteAmountScreen())
    UserModel.splitScreen.step3.bind(on_press=lambda x: deleteAmountScreen())
    UserModel.splitScreen.step4.bind(on_press=lambda x: reloadAmountScreen())

    # UserModel.userMainScreen.startButton.bind(on_press=lambda x: print("Start button pressed"))

    # Screen buttons
    UserModel.splitScreen.sizeScreen.nextButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.baseScreen.nextButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.flavorScreen.nextButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))

    UserModel.splitScreen.sizeScreen.nextButton.bind(on_press=lambda x: enableStep2())
    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: enableStep3())
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: enableStep4())

    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: i2c.run())
    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: print("I2C"))
    # UserModel.amountScreen.doneButton.bind(on_press=lambda x: switch_screen('Split Screen'))
    # UserModel.splitScreen.nextButton1.bind(on_press=lambda x: switch_screen('Base Screen'))
    # UserModel.amountScreen.addButton.bind(on_press=lambda x: switch_screen('Loading Screen'))

    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: getBaseList())
    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: deleteAmountScreen())

    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: getFlavorList())

    # Trigger Amount screen properties
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: reloadAmountScreen())

    UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: amountScreenDone())
    UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: switch_screen("Main Screen"))

    UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x:
        UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.sizeScreen))

def initialize_carousel(split_screen):
    # add all the screens to the carousel
    split_screen.carouselWidget.add_widget(split_screen.sizeScreen)
    split_screen.carouselWidget.add_widget(split_screen.baseScreen)
    split_screen.carouselWidget.add_widget(split_screen.flavorScreen)
    split_screen.carouselWidget.add_widget(split_screen.amountScreen)

# -------------------------------------------------------------------
#                       Size Screen Functions
# -------------------------------------------------------------------
def resetSizeScreen():
    UserModel.splitScreen.sizeScreen.sizeList = []
    UserModel.splitScreen.sizeScreen.toggleButtonSmall.state = 'normal'
    UserModel.splitScreen.sizeScreen.toggleButtonMedium.state = 'normal'
    UserModel.splitScreen.sizeScreen.toggleButtonLarge.state = 'normal'
    UserModel.splitScreen.sizeScreen.nextButton.disabled = True

# -------------------------------------------------------------------
#                       Base Screen Functions
# -------------------------------------------------------------------

# get the list of bases selected by user
def getBaseList():
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for base in UserModel.splitScreen.baseScreen.baseList:
        cursor.execute("INSERT INTO temporary(ingredient) VALUES(?);", (base,))
        connect.commit()

        print("Added " + base + " to Temporary table")
    cursor.close()

    print(UserModel.splitScreen.baseScreen.baseList)

def resetBaseScreen():
    for button in UserModel.splitScreen.baseScreen.baseToggleList:
        button.state = 'normal'
        button.disabled = False

    UserModel.splitScreen.baseScreen.baseList = []
    UserModel.splitScreen.baseScreen.baseToggleList = []
    UserModel.splitScreen.baseScreen.nextButton.disabled = True

# setup the base screen by getting cylinders(bases) from the database


# -------------------------------------------------------------------
#                       Flavor Screen Functions
# -------------------------------------------------------------------

def getFlavorList():
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for flavor in UserModel.splitScreen.flavorScreen.flavorList:
        cursor.execute("INSERT INTO temporary(ingredient) VALUES(?);", (flavor,))
        connect.commit()

        print("Added " + flavor + " to Temporary table")
    cursor.close()

    print(UserModel.splitScreen.flavorScreen.flavorList)


def reloadAmountScreen():
    UserModel.splitScreen.amountScreen.reload()


def deleteAmountScreen():
    UserModel.splitScreen.amountScreen.delete()

def resetFlavorScreen():
    for button in UserModel.splitScreen.flavorScreen.flavorToggleList:
        button.state = 'normal'
        button.disabled = False

    UserModel.splitScreen.flavorScreen.flavorList = []
    UserModel.splitScreen.flavorScreen.flavorToggleList = []


# setup the flavor screen by getting cylinders(flavor) from the database


# -------------------------------------------------------------------
#                       Amount Screen Functions
# -------------------------------------------------------------------


def increment(label_text):
    amount = int(label_text.text)
    amount += 1
    label_text.text = str(amount)


def decrement(label_text):
    amount = int(label_text.text)
    amount -= 1
    label_text.text = str(amount)

def enableStep2():
    UserModel.splitScreen.step2.disabled = False

def enableStep3():
    UserModel.splitScreen.step3.disabled = False

def enableStep4():
    UserModel.splitScreen.step4.disabled = False

def amountScreenDone():
    baseList = UserModel.splitScreen.baseScreen.baseList
    sizeList = UserModel.splitScreen.sizeScreen.sizeList
    # Update temporary table
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for i, flavor in enumerate(UserModel.splitScreen.amountScreen.flavorLayoutList):
        cursor.execute("UPDATE temporary "
                       "SET ml = ?"
                       "WHERE ingredient = ?",
                       (UserModel.splitScreen.amountScreen.flavorLayoutList[i].label_text.text,
                        UserModel.splitScreen.amountScreen.flavorLayoutList[i].flavorName.text))

        # print(UserModel.splitScreen.amountScreen.flavorLayoutList[i].label_text.text)
        # print(UserModel.splitScreen.amountScreen.flavorLayoutList[i].flavorName.text)

    # When 1 base is chosen (slider defaults to 180)
    if len(baseList) == 1 and UserModel.splitScreen.amountScreen.slider.value == 180:
        print("1 Base")
        if len(sizeList) != 0:
            if sizeList[0] == "SMALL":
                cursor.execute("UPDATE temporary "
                               "SET ml = ?"
                               "WHERE ingredient = ?",
                               (10, baseList[0]))
                print(baseList[0])
            elif sizeList[0] == "MEDIUM":
                cursor.execute("UPDATE temporary "
                               "SET ml = ?"
                               "WHERE ingredient = ?",
                               (50, baseList[0]))
            elif sizeList[0] == "LARGE":
                cursor.execute("UPDATE temporary "
                               "SET ml = ?"
                               "WHERE ingredient = ?",
                               (100, baseList[0]))

    elif len(baseList) == 2:
        sliderValue = UserModel.splitScreen.amountScreen.slider.value
        baseProportionList = [sliderValue, 360-sliderValue]
        if len(sizeList) != 0:
            if sizeList[0] == "SMALL":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i]*10/360, baseList[i]))
                    print(baseProportionList[i] * 10 / 360)
                    print(baseList[i])
            elif sizeList[0] == "MEDIUM":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i]*50/360, baseList[i]))
                    print(baseProportionList[i] * 50 / 360)
                    print(baseList[i])
            elif sizeList[0] == "LARGE":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i]*100/360, baseList[i]))
                    print(baseProportionList[i] * 100 / 360)
                    print(baseList[i])

    connect.commit()
    cursor.close()

    # Deselect all previous options
    resetSizeScreen()
    resetBaseScreen()
    resetFlavorScreen()

def printOut():
    print('called')


# -------------------------------------------------------------------
#                       Amount Screen Functions
# -------------------------------------------------------------------

def header_font_size():
    fontSize = Window.width * 0.05
    if fontSize < 23:
        fontSize = 23
    if fontSize > 36:
        fontSize = 36

    return fontSize
