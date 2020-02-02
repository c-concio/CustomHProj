import kivy
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget

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
    nextButton = ObjectProperty(None)


class BaseScreen(Screen):
    nextButton = ObjectProperty(None)


class FlavorScreen(Screen):
    nextButton = ObjectProperty(None)


class SauceOfMonth(Screen):
    pass


class AmountScreen(Screen):
    doneButton = ObjectProperty(None)
    # addButtons = ObjectProperty(None)
    # removeButton = ObjectProperty(None)
    mainGrid = ObjectProperty(None)
    bodyGrid = ObjectProperty(None)
    sliderAnchorLayout = ObjectProperty(None)
    sliderTemplateGrid = ObjectProperty(None)

    # label_text = StringProperty()

    def __init__(self):
        super().__init__()
        # TODO: uncomment
        # self.count = 0
        # self.label_text = str(self.count)
        # self.addButtons.bind(on_press=lambda x: UserController.increment(self))
        # self.removeButton.bind(on_press=lambda x: UserController.decrement(self))
        self.bodyGrid.cols = 1 if Window.width < 425 else 2
        
        # if only one column, the sliderLayout should have the height of the base grid

        #TODO: look inside DB and add flavors
        self.sliderTemplateGrid.add_widget(FlavorsLayout())
        self.sliderTemplateGrid.add_widget(FlavorsLayout())


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


class BaseSliderLayout(AnchorLayout):
    pass


class FlavorsLayout(BoxLayout):
    flavorAddB = ObjectProperty(None)
    flavorRemoveB = ObjectProperty(None)
    label_text = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.label_text.text = "0"
        self.flavorAddB.bind(on_press=lambda x: UserController.increment(self.label_text))
        self.flavorRemoveB.bind(on_press=lambda x: UserController.decrement(self.label_text))



# -------------------------------------------------------------------
#                       Screen Manager
# -------------------------------------------------------------------

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/User/UserScreensKivy.kv')

# TODO: uncomment
# screenManager = ScreenManager()
#
# # initialize User screens
# userMainScreen = UserMainScreen(name="User Main Screen")
# splitScreen = SplitScreen(name="Split Screen")
#
# UserController.initialize_buttons()
# screenManager.add_widget(userMainScreen)
# screenManager.add_widget(splitScreen)
