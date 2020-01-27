from kivy.uix.boxlayout import BoxLayout

from Controller import AdminMainScreenController, MainScreenController
import kivy

from Model import AdminModel, BaseModel

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.properties import ObjectProperty

from kivy.lang import Builder

# Kivy file for Main Screen
Builder.load_file('View/MainScreenKivy.kv')


# //////////////////////////////////////////////////
#                  Screen Classes
# //////////////////////////////////////////////////

class MainScreen(Screen):
    adminButton = ObjectProperty(None)
    baseButton = ObjectProperty(None)


# //////////////////////////////////////////////////
#                  Screen Manager
# //////////////////////////////////////////////////

# initialize Main Screen manager
mainScreenManager = ScreenManager()

# initialize Main Screen
mainScreen = MainScreen(name='Main Screen')

# adminScreen = AdminModel.AdminMainScreen(name="Admin Main Screen")

# initialize Base screen
baseScreen = BaseModel.BaseScreen(name='Base Screen')

mainScreenManager.add_widget(mainScreen)
# mainScreenManager.add_widget(adminScreen)
mainScreenManager.add_widget(baseScreen)

MainScreenController.initialize_buttons()

mainScreenManager.transition = CardTransition()
