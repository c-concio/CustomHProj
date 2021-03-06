import sqlite3
import threading
import time
from tkinter import Button

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from Controller import AdminMainScreenController, DatabaseController
import kivy

from Model import MainModel

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
from kivy.core.window import Window

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/Admin/AdminScreensKivy.kv')


# //////////////////////////////////////////////////
#                  Screen Classes
# //////////////////////////////////////////////////

# classes for all the different admin screens
class AdminMainScreen(Screen):
    inventoryButton = ObjectProperty(None)
    internetButton = ObjectProperty(None)
    powerButton = ObjectProperty(None)
    returnMainScreen = ObjectProperty(None)
    entered = False

    def on_enter(self, *args):
        AdminMainScreenController.initialize_admin_buttons()
        AdminMainScreenController.setup_inventory_screen()


class InventoryScreen(Screen):
    grid = ObjectProperty(None)
    backButton = ObjectProperty(None)
    editIngredientButton = ObjectProperty(None)
    sortToggleButton = ObjectProperty(None)
    entered = False

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.grid.bind(minimum_height=self.grid.setter('height'))

    def on_enter(self, *args):
        AdminMainScreenController.initialize_inventory_buttons()


class InventoryItemTemplate(BoxLayout):
    cylinderButton = ObjectProperty(None)
    ingredientSpinner = ObjectProperty(None)
    ingredientSpinner = ObjectProperty(None)
    percentButton = ObjectProperty(None)
    progressBar = ObjectProperty(None)
    resetButton = ObjectProperty(None)

    def __init__(self, cylinderID):
        super().__init__()
        self.cylinderID = cylinderID
        type = DatabaseController.get_cylinder_type(cylinderID)
        if type == "base":
            with self.canvas.before:
                self.color_widget = Color(0.8, 0.06, 0.06, 0.3)
                self._rectangle = Rectangle()
        else:
            with self.canvas.before:
                self.color_widget = Color(0.2, 0.2, 0.8, 0.25)
                self._rectangle = Rectangle()

    def on_size(self, *args):
        self._rectangle.size = self.size
        self._rectangle.pos = self.pos


class InventoryPopupButtonLayout(BoxLayout):
    ingredientButton = ObjectProperty(None)
    deleteButton = ObjectProperty(None)

    def __init__(self, ingredientID, type):
        super().__init__()
        self.ingredientID = ingredientID
        self.type = type


class AddInventoryPopupLayout(BoxLayout):
    confirmButton = ObjectProperty(None)
    declineButton = ObjectProperty(None)


class ResetMotorPopupLayout(StackLayout):
    upButton = ObjectProperty(None)
    downButton = ObjectProperty(None)
    doneButton = ObjectProperty(None)
    pauseButton = ObjectProperty(None)


# //////////////////////////////////////////////////
#                     Threads
# //////////////////////////////////////////////////

# -------------- Thread Variables ------------------
moveMotorUp = False
moveMotorDown = False
pauseMotor = False
threadLock = threading.Lock()
activeThread = None


# thread that moves the motor up until the moveMotorUp boolean turns False
class MotorUpThread(threading.Thread):
    cylinderID = 0
    cylinderType = "none"

    def __init__(self, cylinderID, cylinderType):
        super().__init__()
        self.cylinderID = cylinderID
        self.cylinderType = cylinderType

    def run(self):
        while True:
            time.sleep(0.01)

            # TODO: add move motor up loop

            threadLock.acquire()
            if not moveMotorUp:
                threadLock.release()
                break

            # move motor and update the database
            if self.cylinderType == "base":
                DatabaseController.add_cylinder_steps(self.cylinderID, self.cylinderType, 10, sqlite3.connect(r'database/pysqlite.db'))
            elif self.cylinderType == "flavor":
                DatabaseController.add_cylinder_steps(self.cylinderID, self.cylinderType, 1, sqlite3.connect(r'database/pysqlite.db'))

            threadLock.release()

        print("Exited up while loop")


# thread that moves the motor down until the moveMotorDown boolean turns False
class MotorDownThread(threading.Thread):
    cylinderID = 0
    cylinderType = "none"

    def __init__(self, cylinderID, cylinderType):
        super().__init__()
        self.cylinderID = cylinderID
        self.cylinderType = cylinderType

    def run(self):
        while True:
            time.sleep(0.01)

            # TODO: add move motor down loop

            threadLock.acquire()
            if not moveMotorDown:
                threadLock.release()
                break

            if self.cylinderType == "base":
                DatabaseController.sub_cylinder_steps(self.cylinderID, 10, sqlite3.connect(r'database/pysqlite.db'))
            elif self.cylinderType == "flavor":
                DatabaseController.sub_cylinder_steps(self.cylinderID, 1, sqlite3.connect(r'database/pysqlite.db'))


            threadLock.release()

        print("Exited down while loop")


# //////////////////////////////////////////////////
#                  Screen Manager
# //////////////////////////////////////////////////

# make the app fullscreen
# Window.fullscreen = 'auto'


# initialize Screen manager
# screenManager = ScreenManager()

# initialize admin screens
adminMainScreen = AdminMainScreen(name='Admin Main Screen')
inventoryScreen = InventoryScreen(name='Inventory Screen')

MainModel.mainScreenManager.add_widget(adminMainScreen)
MainModel.mainScreenManager.add_widget(inventoryScreen)

# popup variable for inventory screen
ingredientPopup = Popup()
addConfirmationPopup = Popup()
deleteConfirmationPopup = Popup()
resetMotorPopup = Popup()

text_input = TextInput()
