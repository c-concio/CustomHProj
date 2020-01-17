from Model import adminScreens

import kivy
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

class ScreenManager():
    # make the app fullscreen
    Window.fullscreen = 'auto'

    # use the kv definitions found in the adminScreensKivy.kv file
    Builder.load_file('View/Admin/adminScreensKivy.kv')

    # initialize Screen manager
    sm = ScreenManager()
    adminMainScreen = adminScreens.AdminMainScreen(name='Admin Main Screen')
    inventoryScreen = adminScreens.AdminMainScreen(name='Inventory Screen')
    internetSettingsScreen = adminScreens.AdminMainScreen(name='Internet Settings Screen')

    # initialize admin screens
    sm.add_widget(adminMainScreen)
    sm.add_widget(inventoryScreen)
    sm.add_widget(internetSettingsScreen)