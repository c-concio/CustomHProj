from Controller import DatabaseController
from Model import AdminModel, DatabaseClass, BaseModel


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    BaseModel.baseScreenManager.transition.direction = 'left'
    BaseModel.baseScreenManager.current = screen_name
    return


def return_screen(screen_name):
    BaseModel.baseScreenManager.transition.direction = 'right'
    BaseModel.baseScreenManager.current = screen_name

# def initialize_buttons():
#
#     # BaseModel.baseScreen()
#     # BaseModel.baseScreen.backButton.bind(on_press=lambda x: return_screen('Main Screen'))
