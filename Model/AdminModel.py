from tkinter import Button

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from Controller import AdminMainScreenController
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


class InventoryScreen(Screen):
    grid = ObjectProperty(None)
    backButton = ObjectProperty(None)
    editIngredientButton = ObjectProperty(None)
    sortToggleButton = ObjectProperty(None)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.grid.bind(minimum_height=self.grid.setter('height'))


class InternetSettingsScreen(Screen):
    pass


class InventoryItemTemplate(BoxLayout):
    cylinderButton = ObjectProperty(None)
    ingredientSpinner = ObjectProperty(None)
    percentButton = ObjectProperty(None)
    progressBar = ObjectProperty(None)
    resetButton = ObjectProperty(None)

    def __init__(self, cylinderID):
        super().__init__()
        self.cylinderID = cylinderID


class InventoryPopupButtonLayout(BoxLayout):
    ingredientButton = ObjectProperty(None)
    deleteButton = ObjectProperty(None)


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
internetSettingsScreen = InternetSettingsScreen(name='Internet Settings Screen')

AdminMainScreenController.setup_inventory_screen()
AdminMainScreenController.initialize_buttons()

MainModel.mainScreenManager.add_widget(adminMainScreen)
MainModel.mainScreenManager.add_widget(inventoryScreen)
MainModel.mainScreenManager.add_widget(internetSettingsScreen)

# popup variable for inventory screen
popup = Popup(title='Ingredients', size_hint=(None, None), size=(400, 400))

text_input = TextInput()
