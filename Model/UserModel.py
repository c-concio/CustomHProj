import kivy
from kivy.clock import Clock
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
from Model import BaseModel

kivy.require('1.9.0')

LabelBase.register(name="Pacifico", fn_regular="Pacifico.ttf")
LabelBase.register(name="OstrichSans", fn_regular="ostrich-regular.ttf")


# -------------------------------------------------------------------
#                       Screen Classes
# -------------------------------------------------------------------


class UserMainScreen(Screen):
    startButton = ObjectProperty(None)


class SizeScreen(Screen):
    pass
    # nextButton1 = ObjectProperty(None)


#class BaseScreen(Screen):
#    nextButton2 = ObjectProperty(None)


class FlavorScreen(Screen):
    nextButton3 = ObjectProperty(None)


class SauceOfMonth(Screen):
    pass


class AmountScreen(Screen):
    doneButton = ObjectProperty(None)
    addButtons = ObjectProperty(None)
    removeButton = ObjectProperty(None)

    label_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__()
        self.count = 0
        self.label_text = str(self.count)
        self.addButtons.bind(on_press=lambda x: UserController.increment(self))
        self.removeButton.bind(on_press=lambda x: UserController.decrement(self))


class SplitScreen(Screen):
    step1 = ObjectProperty(None)
    step2 = ObjectProperty(None)
    step3 = ObjectProperty(None)
    step4 = ObjectProperty(None)
    carouselScreen = ObjectProperty(None)
    baseScreen = ObjectProperty(None)
    flavorScreen = ObjectProperty(None)
    sizeScreen = ObjectProperty(None)
    nextButton1 = ObjectProperty(None)
    nextButton2 = ObjectProperty(None)
    nextButton3 = ObjectProperty(None)


# -------------------------------------------------------------------
#                       Screen Manager
# -------------------------------------------------------------------

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/User/UserScreensKivy.kv')

screenManager = ScreenManager()

# initialize User screens
userMainScreen = UserMainScreen(name="User Main Screen")
splitScreen = SplitScreen(name="Split Screen")

UserController.initialize_buttons()
screenManager.add_widget(userMainScreen)
# screenManager.add_widget(sizeScreen)
# screenManager.add_widget(baseScreen)
# screenManager.add_widget(flavorScreen)
# screenManager.add_widget(sauceOfMonth)
# screenManager.add_widget(amountScreen)
screenManager.add_widget(splitScreen)
