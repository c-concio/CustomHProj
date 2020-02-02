from Controller import DatabaseController
from Model import AdminModel, BaseModel, DatabaseClass, MainModel, FlavorModel, UserModel


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
    MainModel.mainScreen.userButton.bind(on_press=lambda x: switch_screen('Split Screen'))


    # Carousel screens
    UserModel.splitScreen.step1.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.sizeScreen))
    UserModel.splitScreen.step2.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.step3.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.step4.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))

    # UserModel.userMainScreen.startButton.bind(on_press=lambda x: print("Start button pressed"))
    UserModel.splitScreen.sizeScreen.nextButton.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))

    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: getBaseList())
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: getFlavorList())

    # BaseModel.baseScreen.backButton.bind(on_press=lambda x: return_screen('Main Screen'))
