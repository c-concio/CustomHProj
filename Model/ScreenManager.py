from Model import AdminScreens
from Controller import AdminMainScreenController

import kivy
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window


# make the app fullscreen
Window.fullscreen = 'auto'

# use the kv definitions found in the AdminScreensKivy.kv file
Builder.load_file('View/Admin/AdminScreensKivy.kv')

# initialize Screen manager
screenManager = ScreenManager()

# initialize admin screens
adminMainScreen = AdminScreens.AdminMainScreen(name='Admin Main Screen')
inventoryScreen = AdminScreens.InventoryScreen(name='Inventory Screen')
internetSettingsScreen = AdminScreens.InternetSettingsScreen(name='Internet Settings Screen')
screenManager.add_widget(adminMainScreen)
screenManager.add_widget(inventoryScreen)
screenManager.add_widget(internetSettingsScreen)