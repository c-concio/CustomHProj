import kivy
from Model import AdminModel
from kivy.uix.screenmanager import Screen


# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    AdminModel.screenManager.transition.direction = 'left'
    AdminModel.screenManager.current = screen_name
    return

def return_screen(screen_name):
    AdminModel.screenManager.transition.direction = 'right'
    AdminModel.screenManager.current = screen_name

# function that powers off application
def quit_application():
    raise SystemExit
