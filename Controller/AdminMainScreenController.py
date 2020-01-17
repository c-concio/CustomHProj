import kivy
from Model import ScreenManager
from kivy.uix.screenmanager import Screen


# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screenName):
    ScreenManager.screenManager.current = screenName
