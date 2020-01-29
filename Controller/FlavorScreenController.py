from Controller import DatabaseController
from Model import AdminModel, DatabaseClass, BaseModel, MainModel


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'left'
    MainModel.mainScreenManager.current = screen_name
    return
#
#
# def return_screen(screen_name):
#     BaseModel.baseScreenManager.transition.direction = 'right'
#     BaseModel.baseScreenManager.current = screen_name

# def initialize_buttons():
#     # BaseModel.baseScreen.nextButton.bind(on_press=lambda x: switch_screen("Flavor Screen"))