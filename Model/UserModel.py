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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.animation import Animation


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
    toggleButtonSmall = ObjectProperty(None)
    toggleButtonMedium = ObjectProperty(None)
    toggleButtonLarge = ObjectProperty(None)
    nextButton = ObjectProperty(None)
    sizeList = []

    def __init__(self, **kwargs):
        super(SizeScreen, self).__init__(**kwargs)

        self.toggleButtonSmall.bind(on_press=self.saveSize)
        self.toggleButtonMedium.bind(on_press=self.saveSize)
        self.toggleButtonLarge.bind(on_press=self.saveSize)

    def saveSize(self, instance):
        # Save size of cup
        if instance.state == 'down':
            self.sizeList.append(instance.text)
            print("Added " + instance.text)
        else:
            try:
                self.sizeList.remove(instance.text)
                print("Removed " + instance.text)
            except:
                print("Could not remove base, it did not exist")

        if len(self.sizeList) < 1:
            self.nextButton.disabled = True
        else:
            self.nextButton.disabled = False


class BaseScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty()
    nextButton = ObjectProperty()
    flavourOfMonthButton = ObjectProperty()
    baseList = []
    baseToggleList = []

    # backButton = ObjectProperty(None)

    # def btn(self):
    #     UserController.showPopupWindow()

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
            print("Width")
            self.grid.cols = 1
        else:
            self.grid.cols = 2

        # Dynamic buttons
        for i, base in enumerate(bases):
            button = ToggleButton(text=str(base[1]))
            self.baseToggleList.append(button)
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

        if len(self.baseList) < 1:
            self.nextButton.disabled = True
        else:
            self.nextButton.disabled = False

        # Disable other buttons when 2 bases are chosen
        if len(self.baseList) >= 2:
            for button in self.baseToggleList:
                if button.text not in self.baseList:
                    button.disabled = True
                    # print("This button disabled: " + button.text)
        else:
            for button in self.baseToggleList:
                if button.text not in self.baseList:
                    button.disabled = False
                    # print("This button recovered: " + button.text)


class SauceOfMonth(Screen):
    doneButton: ObjectProperty(None)
    closeButton: ObjectProperty(None)
    # title: ObjectProperty(None)
    # separator_height: ObjectProperty()

    # TODO get sauce choices from db


class FlavorScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty()
    nextButton = ObjectProperty()
    flavorList = []
    flavorToggleList = []

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
            self.flavorToggleList.append(button)
            self.grid.add_widget(button)

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

        # Disable other buttons when 3 flavors are chosen
        if len(self.flavorList) >= 3:
            for button in self.flavorToggleList:
                if button.text not in self.flavorList:
                    button.disabled = True
                    # print("This button disabled: " + button.text)
        else:
            for button in self.flavorToggleList:
                if button.text not in self.flavorList:
                    button.disabled = False
                    # print("This button recovered: " + button.text)


class AmountScreen(Screen):
    mainGrid = ObjectProperty(None)
    bodyGrid = ObjectProperty(None)
    sliderAnchorLayout = ObjectProperty(None)
    sliderTemplateGrid = ObjectProperty(None)
    slider = ObjectProperty(None)
    sliderExist = True
    doneButton = ObjectProperty(None)
    base1 = ObjectProperty(None)
    base2 = ObjectProperty(None)
    baseChartLayout = ObjectProperty(None)
    baseChart = ObjectProperty(None)
    flavorLayoutList = []

    def __init__(self):
        super().__init__()
        # TODO: uncomment
        # self.count = 0
        # self.label_text = str(self.count)
        # self.addButtons.bind(on_press=lambda x: UserController.increment(self))
        # self.removeButton.bind(on_press=lambda x: UserController.decrement(self))
        self.bodyGrid.cols = 1 if Window.width < 425 else 2

        # if only one column, the sliderLayout should have the height of the base grid

        # TODO: look inside DB and add flavors
        # self.sliderTemplateGrid.add_widget(FlavorsLayout("Flavor 1"))

    def reload(self):

        # Remove slider if only 1 base chosen
        if (len(splitScreen.baseScreen.baseList) <= 1):
            self.sliderTemplateGrid.remove_widget(self.slider)
            self.sliderExist = False
            # print(len(splitScreen.baseScreen.baseList))

        # Add slider when slider was removed and chosen bases becomes 2
        if (len(splitScreen.baseScreen.baseList) > 1 and self.sliderExist == False):
            self.sliderTemplateGrid.add_widget(self.slider)
            # print("Added slider")

        try:
            self.base1.text = splitScreen.baseScreen.baseList[0]
        except:
            self.base1.text = ""
            print("Nothing inside list")

        try:
            self.base2.text = splitScreen.baseScreen.baseList[1]
        except:
            self.base2.text = ""
            print("No second base was chosen")

        # Show flavors based on user selection
        for i, flavor in enumerate(splitScreen.flavorScreen.flavorList):
            try:
                self.flavorLayoutList.append(FlavorsLayout(flavor))
                self.sliderTemplateGrid.add_widget(self.flavorLayoutList[i])
            except:
                print("Flavor already added")

    def delete(self):
        # Delete flavors when user deselects flavors
        for i, flavor in enumerate(splitScreen.flavorScreen.flavorList):
            try:
                self.sliderTemplateGrid.remove_widget(self.flavorLayoutList[i])
                self.flavorLayoutList.remove(FlavorsLayout(flavor))
            except:
                print("Flavor already removed")

        if (len(splitScreen.baseScreen.baseList) <= 1):
            self.baseChartLayout.remove_widget(self.baseChart)
            print("Removed chart")


class ConfirmScreen(Screen):
    orderButton = ObjectProperty(None)
    confirmLayout = ObjectProperty(None)


class loadingPopup(BoxLayout):
    gif = ObjectProperty(None)


# class CProgressBar(Label):
#     angle = NumericProperty(0)
#     startCount = NumericProperty(20)
#     Count = NumericProperty()
#
#     def __init__(self, **kwargs):
#         super(CProgressBar, self).__init__(**kwargs)
#         Clock.schedule_once(self.set_Circle, 0.1)
#         self.Count = self.startCount
#
#     def set_Circle(self, dt):
#         self.angle = self.angle + dt * 360
#         if self.angle >= 360:
#             self.angle = 0
#             self.Count = self.Count - 1
#         if self.Count > 0:
#             Clock.schedule_once(self.set_Circle, 1.0 / 360)




class SplitScreen(Screen):
    carouselWidget = ObjectProperty(None)
    step1 = ObjectProperty(None)
    step2 = ObjectProperty(None)
    step3 = ObjectProperty(None)
    step4 = ObjectProperty(None)
    step5 = ObjectProperty(None)

    def __init__(self, name):
        super().__init__()
        # screens to be put in carousel
        self.sizeScreen = SizeScreen()
        self.baseScreen = BaseScreen()
        # self.flavorOfMonthScreen = FlavorOfMonth()
        self.flavorScreen = FlavorScreen()
        self.amountScreen = AmountScreen()
        self.confirmScreen = ConfirmScreen()
        UserController.initialize_carousel(self)
        self.name = name


class BaseSliderLayout(AnchorLayout):
    pass


class FlavorsLayout(BoxLayout):
    flavorAddB = ObjectProperty(None)
    flavorRemoveB = ObjectProperty(None)
    label_text = ObjectProperty(None)
    flavorName = ObjectProperty(None)

    def __init__(self, name):
        super().__init__()
        self.label_text.text = "0"
        self.flavorAddB.bind(on_press=lambda x: UserController.increment(self.label_text))
        self.flavorRemoveB.bind(on_press=lambda x: UserController.decrement(self.label_text))
        self.flavorName.text = name


# -------------------------------------------------------------------
#                       Screen Manager
# -------------------------------------------------------------------

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/User/UserScreensKivy.kv')

# screenManager = ScreenManager()

# initialize User screens
userMainScreen = UserMainScreen(name="User Main Screen")
splitScreen = SplitScreen(name="Split Screen")
sizeScreen = SizeScreen(name="Size Screen")
# sauceOfMonthScreen = SauceOfMonth(name="Flavor of The Month")
# loadingScreen = LoadingScreen(name="Loading Screen")
# baseScreen = BaseScreen(name="Base Screen")
# flavorScreen = FlavorScreen(name="Flavor Screen")
# amountScreen = AmountScreen(name="Amount Screen")

UserController.initialize_buttons()
# screenManager.add_widget(userMainScreen)
# screenManager.add_widget(splitScreen)
