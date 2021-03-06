import kivy
import pymysql
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase

from kivy.uix.widget import Widget

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
    qrButton = ObjectProperty(None)


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
            self.sizeList = []
            self.sizeList.append(instance.text)
            print("Added " + instance.text)
        else:
            try:
                self.sizeList.remove(instance.text)
                print("Removed " + instance.text)
            except:
                print("Could not remove base, it did not exist")

        # Next button enable/disable
        if len(self.sizeList) < 1:
            self.nextButton.disabled = True
            self.nextButton.text = ""
            self.nextButton.colour = (1, 1, 1, 0)
        else:
            self.nextButton.disabled = False
            self.nextButton.text = "Next"
            self.nextButton.colour = (1, 1, 1, 0.6)


class BaseScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty()
    nextButton = ObjectProperty()
    sauceOfMonthButton = ObjectProperty()
    baseList = []
    baseToggleList = []


    # Get ingredient names from database
    # Create buttons dynamically based on the 'cylinder' table
    def createButtons(self):
        self.baseList.clear()
        self.baseToggleList.clear()
        sizeList = splitScreen.sizeScreen.sizeList
        # self.sauceOfMonthButton.colour = (1, 1, 1, 0.6)

        connect = DatabaseClass.conn
        cursor = connect.cursor()

        sqlBase = ""
        try:
            if sizeList[0] == "SMALL":
                sqlBase = "SELECT DISTINCT ingredient FROM cylinder WHERE type='base' AND steps > 10;"
            elif sizeList[0] == "MEDIUM":
                sqlBase = "SELECT DISTINCT ingredient FROM cylinder WHERE type='base' AND steps > 50;"
            elif sizeList[0] == "LARGE":
                sqlBase = "SELECT DISTINCT ingredient FROM cylinder WHERE type='base' AND steps > 100;"
        except:
            print("No size selected")

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
        for i, items in enumerate(bases):
            for base in items:
                if base != "None":
                    button = ToggleButton(text=str(base))
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
            self.nextButton.text = ""
            self.nextButton.colour = (1, 1, 1, 0)
        else:
            self.nextButton.disabled = False
            self.nextButton.text = "Next"
            self.nextButton.colour = (1, 1, 1, 0.6)

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


# class SauceOfMonth(Screen):
#     doneButton: ObjectProperty(None)
#     closeButton: ObjectProperty(None)
#     grid = ObjectProperty(None)
#     sauceList = []
#     sauceToggleList = []
#     # title: ObjectProperty(None)
#     # separator_height: ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super(SauceOfMonth, self).__init__(**kwargs)
#         self.doneButton.colour = (1, 1, 1, 0.6)
#
#         try:
#             conn = pymysql.connect(host='127.0.0.1',
#                                    user='root',
#                                    password='customh',
#                                    db='cylinder')
#             cursor = conn.cursor()
#
#             sqlOnline = "SELECT * FROM online ORDER BY count DESC LIMIT 4;"
#             cursor.execute(sqlOnline)
#             rows = cursor.fetchall()
#
#             cursor.close()
#
#             # If screen width is small, have 1 column
#             if (Window.width <= 320):
#                 print("Width")
#                 self.grid.cols = 1
#             else:
#                 self.grid.cols = 2
#
#             # Get top 4 recipes
#             for row in rows:
#                 sauce = ""
#                 for i in range(1, 6):
#                     # print(row[i])
#                     if row[i] is not None:
#                         sauce += row[i] + " "
#                 button = ToggleButton(text=str(sauce))
#                 button.text_size = self.width, None
#                 self.sauceToggleList.append(button)
#                 self.grid.add_widget(button)
#                 button.bind(on_press=self.saveOptions)
#
#
#         except:
#             print("No connection to online database")
#
#     def updateButtons(self):
#         self.grid.clear_widgets()
#         self.sauceList.clear()
#         self.sauceToggleList.clear()
#         conn = pymysql.connect(host='127.0.0.1',
#                                user='root',
#                                password='customh',
#                                db='cylinder')
#         cursor = conn.cursor()
#
#         sqlOnline = "SELECT * FROM online ORDER BY count DESC LIMIT 4;"
#         cursor.execute(sqlOnline)
#         rows = cursor.fetchall()
#
#         cursor.close()
#
#         # If screen width is small, have 1 column
#         if (Window.width <= 320):
#             print("Width")
#             self.grid.cols = 1
#         else:
#             self.grid.cols = 2
#
#         # Get top 4 recipes
#         for row in rows:
#             sauce = ""
#             for i in range(1, 6):
#                 # print(row[i])
#                 if row[i] is not None:
#                     sauce += row[i] + " "
#             button = ToggleButton(text=str(sauce))
#             button.text_size = self.width, None
#             self.sauceToggleList.append(button)
#             self.grid.add_widget(button)
#             button.bind(on_press=self.saveOptions)
#
#     def saveOptions(self, instance):
#         # Save the sauce name in a list to use for the final order
#         if instance.state == 'down':
#             self.sauceList.append(instance.text)
#             print("Added " + instance.text)
#         else:
#             try:
#                 self.sauceList.remove(instance.text)
#                 print("Removed " + instance.text)
#             except:
#                 print("Could not remove sauce, it did not exist")
#
#         if len(self.sauceList) < 1:
#             self.doneButton.disabled = True
#             self.doneButton.text = ""
#             self.doneButton.colour = (1, 1, 1, 0)
#         else:
#             self.doneButton.disabled = False
#             self.doneButton.text = "Done"
#             self.doneButton.colour = (1, 1, 1, 0.6)
#
#         # Disable other buttons when 1 sauce is chosen
#         if len(self.sauceList) >= 1:
#             for button in self.sauceToggleList:
#                 if button.text not in self.sauceList:
#                     button.disabled = True
#                     # print("This button disabled: " + button.text)
#         else:
#             for button in self.sauceToggleList:
#                 if button.text not in self.sauceList:
#                     button.disabled = False
#                     # print("This button recovered: " + button.text)


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
        self.nextButton.colour = (1, 1, 1, 0.6)
        connect = DatabaseClass.conn
        cursor = connect.cursor()

        sqlFlavor = "SELECT DISTINCT ingredient FROM cylinder WHERE type='flavor' AND steps > 10;"
        cursor.execute(sqlFlavor)
        flavors = cursor.fetchall()

        cursor.close()

        # If screen width is small, have 1 column
        if (Window.width <= 320):
            print("Width")
            self.grid.cols = 1
        else:
            self.grid.cols = 2

        # Dynamic buttons
        for i, items in enumerate(flavors):
            for flavor in items:
                if flavor != "None":
                    button = ToggleButton(text=str(flavor))
                    self.flavorToggleList.append(button)
                    self.grid.add_widget(button)
                    button.bind(on_press=self.saveButtonName)
    def createButtons(self):
        self.flavorList.clear()
        self.flavorToggleList.clear()

        self.nextButton.colour = (1, 1, 1, 0.6)
        connect = DatabaseClass.conn
        cursor = connect.cursor()

        sqlFlavor = "SELECT DISTINCT ingredient FROM cylinder WHERE type='flavor' AND steps > 10;"
        cursor.execute(sqlFlavor)
        flavors = cursor.fetchall()

        cursor.close()

        # If screen width is small, have 1 column
        if (Window.width <= 320):
            print("Width")
            self.grid.cols = 1
        else:
            self.grid.cols = 2

        # Dynamic buttons
        for i, items in enumerate(flavors):
            for flavor in items:
                if flavor != "None":
                    button = ToggleButton(text=str(flavor))
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
    doneButton = ObjectProperty(None)
    scroll = ObjectProperty(None)
    box = ObjectProperty(None)
    built = False
    flavorLayoutList = []


class AmountGridLayout(GridLayout):
    pass


class ConfirmScreen(Screen):
    orderButton = ObjectProperty(None)
    confirmLayout = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.orderButton.colour = (1, 1, 1, 0.6)


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
        self.name = name
        UserController.initialize_main_screen_buttons()

    def on_pre_enter(self, *args):
        # screens to be put in carousel
        self.sizeScreen = SizeScreen()
        self.baseScreen = BaseScreen()
        self.flavorScreen = FlavorScreen()
        self.amountScreen = AmountScreen()
        self.confirmScreen = ConfirmScreen()
        UserController.initialize_carousel(self)
        UserController.initialize_buttons()
        self.carouselWidget.load_slide(self.sizeScreen)

        # check if the 
        3


class FlavorsLayout(GridLayout):
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


class BaseGridTemplate1(GridLayout):
    baseLabel1 = ObjectProperty(None)


class BaseGridTemplate2(GridLayout):
    baseLabel1 = ObjectProperty(None)
    baseLabel2 = ObjectProperty(None)
    slider = ObjectProperty(None)


class BaseStackTemplate1(GridLayout):
    baseLabel1 = ObjectProperty(None)


class AmountPieChart(Widget):
    pass


class BaseStackTemplate2(GridLayout):
    baseLabel1 = ObjectProperty(None)
    baseLabel2 = ObjectProperty(None)
    slider = ObjectProperty(None)
    pie = AmountPieChart


class DoneRoundedButton1(Button):
    pass


class DoneRoundedButton2(Button):
    pass


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

# screenManager.add_widget(userMainScreen)
# screenManager.add_widget(splitScreen)


popup = Popup(title="", separator_height=0, size_hint=(None, None), size=(Window.width * 0.5, Window.height * 0.8),
              content=loadingPopup())

popup.auto_dismiss = False
