from Controller import DatabaseController
from Model import AdminModel, DatabaseClass, MainModel, UserModel


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
    MainModel.mainScreen.userButton.bind(on_press=lambda x: switch_screen('Split Screen'))

    # UserModel.userMainScreen.startButton.bind(on_press=lambda x: print("Start button pressed"))


    # BaseModel.baseScreen.backButton.bind(on_press=lambda x: return_screen('Main Screen'))
