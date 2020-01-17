from Controller import adminMainScreenController
import kivy
#:import adminScreens
kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen

controller = adminMainScreenController
class AdminMainScreen(Screen):
    pass


class InventoryScreen(Screen):
    pass


class InternetSettingsScreen(Screen):
    pass
