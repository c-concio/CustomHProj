import kivy
from kivy.clock import Clock
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

from CustomHProj.Model import UserModel

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
    UserModel.userMainScreen.startButton.bind(on_press=lambda x: switch_screen('Cup Size Screen'))
    UserModel.sizeScreen.nextButton1.bind(on_press=lambda x: switch_screen('Base Screen'))
    UserModel.baseScreen.nextButton2.bind(on_press=lambda x: switch_screen('Flavor Screen'))
    UserModel.flavorScreen.nextButton3.bind(on_press=lambda x: switch_screen('Amount Adjustment Screen'))
    UserModel.amountScreen.doneButton.bind(on_press=lambda x: switch_screen('Split Screen'))
    # UserModel.amountScreen.addButton.bind(on_press=lambda x: switch_screen('Loading Screen'))




# -------------------------------------------------------------------
#                       Base Screen Functions
# -------------------------------------------------------------------

# setup the base screen by getting cylinders(bases) from the database


# -------------------------------------------------------------------
#                       Flavor Screen Functions
# -------------------------------------------------------------------

# setup the flavor screen by getting cylinders(flavor) from the database


# -------------------------------------------------------------------
#                       Amount Screen Functions
# -------------------------------------------------------------------




def increment(self, *args):
    self.count += 1
    self.label_text = str(self.count)
    self.label_text


def decrement(self, *args):
    self.count -= 1
    self.label_text = str(self.count)
    self.label_text


