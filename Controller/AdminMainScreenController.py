import kivy
from Model import ScreenManager
from kivy.uix.screenmanager import Screen


# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    ScreenManager.screenManager.current = screen_name
    return

# function that powers off application
def quit_application():
    raise SystemExit
