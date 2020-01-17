from Controller import AdminMainScreenController
from Model import ScreenManager
import kivy

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


# classes for all the different admin screens
class AdminMainScreen(Screen):
    editInventoryButton = ObjectProperty(None)

    def initialize_buttons(self):
        self.editInventoryButton.bind(on_press=self.button_change)

    def button_change(self, instance):
        AdminMainScreenController.switch_screen('Inventory Screen')


class InventoryScreen(Screen):
    pass


class InternetSettingsScreen(Screen):
    pass
