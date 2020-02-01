from Controller import DatabaseController
from Model import AdminModel, BaseModel, DatabaseClass, MainModel, FlavorModel


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


# get the list of bases selected by user
def getBaseList():
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for base in BaseModel.baseScreen.baseList:
        cursor.execute("INSERT INTO temporary(ingredient) VALUES(?);", (base,))
        connect.commit()

        print("Added " + base + " to Temporary table")
    cursor.close()

    print(BaseModel.baseScreen.baseList)


def getFlavorList():
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for flavor in FlavorModel.flavorScreen.flavorList:
        cursor.execute("INSERT INTO temporary(ingredient) VALUES(?);", (flavor,))
        connect.commit()

        print("Added " + flavor + " to Temporary table")
    cursor.close()

    print(FlavorModel.flavorScreen.flavorList)


def initialize_buttons():
    MainModel.mainScreen.adminButton.bind(on_press=lambda x: switch_screen('Admin Main Screen'))
    MainModel.mainScreen.baseButton.bind(on_press=lambda x: switch_screen('Base Screen'))
    MainModel.baseScreen.nextButton.bind(on_press=lambda x: switch_screen('Flavor Screen'))

    MainModel.baseScreen.nextButton.bind(on_press=lambda x: getBaseList())
    MainModel.flavorScreen.nextButton.bind(on_press=lambda x: getFlavorList())

    # BaseModel.baseScreen.backButton.bind(on_press=lambda x: return_screen('Main Screen'))
