import kivy
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase

from Controller import UserController
from Model import DatabaseClass

kivy.require('1.9.0')

LabelBase.register(name="Pacifico", fn_regular="Pacifico.ttf")
LabelBase.register(name="OstrichSans", fn_regular="ostrich-regular.ttf")


# -------------------------------------------------------------------
#                       Screen Classes
# -------------------------------------------------------------------


class UserMainScreen(Screen):
    startButton = ObjectProperty(None)


class SizeScreen(Screen):
    nextButton = ObjectProperty(None)


class BaseScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty()
    nextButton = ObjectProperty(None)
    baseList = []

    # backButton = ObjectProperty(None)

    # Get ingredient names from database
    # Create buttons dynamically based on the 'cylinder' table
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)

        connect = DatabaseClass.conn

        cursor = connect.cursor()

        sqlBase = "SELECT * FROM cylinder WHERE type='Base';"
        cursor.execute(sqlBase)
        bases = cursor.fetchall()

        cursor.close()

        # If screen width is small, have 1 column
        if (Window.width <= 320):
            self.grid.cols = 1
        else:
            self.grid.cols = 2

        # Dynamic buttons
        for i, base in enumerate(bases):
            button = ToggleButton(text=str(base[1]))
            self.grid.add_widget(button)

            button.bind(on_press=self.saveButtonName)

    def saveButtonName(self, instance):
        # Save the base name in a list to use for the final order
        if instance.state == 'down':
            self.baseList.append(instance.text)
            print("Added " + instance.text)
        else:
            try:
                self.baseList.remove(instance.text)
                print("Removed " + instance.text)
            except:
                print("Could not remove base, it did not exist")


class FlavorScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty(None)
    nextButton = ObjectProperty(None)
    flavorList = []

    # backButton = ObjectProperty(None)

    # Get ingredient names from database
    # Create buttons dynamically based on the 'cylinder' table
    def __init__(self, **kwargs):
        super(FlavorScreen, self).__init__(**kwargs)
        connect = DatabaseClass.conn
        cursor = connect.cursor()

        sqlFlavor = "SELECT * FROM cylinder WHERE type='Flavor';"
        cursor.execute(sqlFlavor)
        bases = cursor.fetchall()

        cursor.close()

        # If screen width is small, have 1 column
        if (Window.width <= 320):
            print("Width")
            self.grid.cols = 1
        else:
            self.grid.cols = 2

        # Dynamic buttons
        for i, base in enumerate(bases):
            button = ToggleButton(text=str(base[1]))
            self.grid.add_widget(button)
            # print("Base " + str(i) + ": " + base[1])

            button.bind(on_press=self.saveButtonName)

    def saveButtonName(self, instance):
        # Save the flavor name in a list to use for the final order
        if instance.state == 'down':
            self.flavorList.append(instance.text)
            print("Added " + instance.text)
        else:
            try:
                self.flavorList.remove(instance.text)
                print("Removed " + instance.text)
            except:
                print("Could not remove base, it did not exist")


class SauceOfMonth(Screen):
    pass


class AmountScreen(Screen):
    doneButton = ObjectProperty(None)
    addButtons = ObjectProperty(None)
    removeButton = ObjectProperty(None)

    label_text = StringProperty()

    def __init__(self):
        super().__init__()
        self.count = 0
        self.label_text = str(self.count)
        self.addButtons.bind(on_press=lambda x: UserController.increment(self))
        self.removeButton.bind(on_press=lambda x: UserController.decrement(self))



class SplitScreen(Screen):
    carouselWidget = ObjectProperty(None)
    step1 = ObjectProperty(None)
    step2 = ObjectProperty(None)
    step3 = ObjectProperty(None)
    step4 = ObjectProperty(None)



    def __init__(self, name):
        super().__init__()
        # screens to be put in carousel
        self.sizeScreen = SizeScreen()
        self.baseScreen = BaseScreen()
        self.flavorScreen = FlavorScreen()
        self.amountScreen = AmountScreen()
        UserController.initialize_carousel(self)
        self.name = name


# -------------------------------------------------------------------
#                       Screen Manager
# -------------------------------------------------------------------

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/User/UserScreensKivy.kv')

screenManager = ScreenManager()

# initialize User screens
userMainScreen = UserMainScreen(name="User Main Screen")
splitScreen = SplitScreen(name="Split Screen")
baseScreen = BaseScreen(name="Base Screen")
flavorScreen = FlavorScreen(name="Flavor screen")

UserController.initialize_buttons()
screenManager.add_widget(userMainScreen)
# screenManager.add_widget(splitScreen)
