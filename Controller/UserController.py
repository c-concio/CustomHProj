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
from Model import UserModel, DatabaseClass

kivy.require('1.9.0')


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    UserModel.screenManager.transition.direction = 'left'
    UserModel.screenManager.current = screen_name
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

    UserModel.userMainScreen.startButton.bind(on_press=lambda x: switch_screen('Split Screen'))
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
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: getFlavorList())

    # Trigger Amount screen properties
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: reloadAmountScreen())


def initialize_carousel(split_screen):
    # add all the screens to the carousel
    split_screen.carouselWidget.add_widget(split_screen.sizeScreen)
    split_screen.carouselWidget.add_widget(split_screen.baseScreen)
    split_screen.carouselWidget.add_widget(split_screen.flavorScreen)
    split_screen.carouselWidget.add_widget(split_screen.amountScreen)


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
