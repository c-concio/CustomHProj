from Controller import AdminMainScreenController
from Model import ScreenManager
import kivy

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


# classes for all the different admin screens
class AdminMainScreen(Screen):
    inventoryButton = ObjectProperty(None)
    internetButton = ObjectProperty(None)
    powerButton = ObjectProperty(None)

    # Button switches to the
    def initialize_buttons(self):
        self.inventoryButton.bind(on_press=lambda x: AdminMainScreenController.switch_screen('Inventory Screen'))
        self.internetButton.bind(on_press=lambda x: AdminMainScreenController.switch_screen('Internet Settings Screen'))
        self.powerButton.bind(on_press=AdminMainScreenController.quit_application)


class InventoryScreen(Screen):
    # TODO: Make inventory items then grid them up
    grid = ObjectProperty(None)

    def add_template(self):
        self.grid.add_widget(InventoryItemTemplate())
        self.grid.add_widget(InventoryItemTemplate())
        self.grid.add_widget(InventoryItemTemplate())


class InternetSettingsScreen(Screen):
    pass


class InventoryItemTemplate(FloatLayout):
    pass


