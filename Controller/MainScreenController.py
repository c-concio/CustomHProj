from Controller import DatabaseController
from Model import MainModel, BaseModel


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'left'
    MainModel.mainScreenManager.current = screen_name
    return


def return_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'right'
    MainModel.mainScreenManager.current = screen_name

def initialize_buttons():
    MainModel.mainScreen.adminButton.bind(on_press=lambda x: switch_screen('Admin Main Screen'))
    MainModel.mainScreen.baseButton.bind(on_press=lambda x: switch_screen('Base Screen'))
    MainModel.baseScreen.nextButton.bind(on_press=lambda x: switch_screen('Flavor Screen'))

    # BaseModel.baseScreen.backButton.bind(on_press=lambda x: return_screen('Main Screen'))
