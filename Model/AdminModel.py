from Controller import AdminMainScreenController
import kivy

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
from kivy.core.window import Window



# //////////////////////////////////////////////////
#                  Screen Classes
# //////////////////////////////////////////////////

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
        inventoryScreen.backButton.bind(on_press=lambda x: AdminMainScreenController.return_screen('Admin Main Screen'))


class InventoryScreen(Screen):
    # TODO: Make inventory items then grid them up
    grid = ObjectProperty(None)
    backButton = ObjectProperty(None)

    def add_template(self):
        self.grid.add_widget(InventoryItemTemplate())


class InternetSettingsScreen(Screen):
    pass


class InventoryItemTemplate(FloatLayout):
    pass

# //////////////////////////////////////////////////
#                  Screen Manager
# //////////////////////////////////////////////////

# make the app fullscreen
# Window.fullscreen = 'auto'

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/Admin/AdminScreensKivy.kv')

# initialize Screen manager
screenManager = ScreenManager()

# initialize admin screens
adminMainScreen = AdminMainScreen(name='Admin Main Screen')
inventoryScreen = InventoryScreen(name='Inventory Screen')
internetSettingsScreen = InternetSettingsScreen(name='Internet Settings Screen')
screenManager.add_widget(adminMainScreen)
screenManager.add_widget(inventoryScreen)
screenManager.add_widget(internetSettingsScreen)
screenManager.transition = CardTransition()

