import sqlite3

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from Controller import AdminMainScreenController, MainScreenController, BaseScreenController
import kivy

from Model import MainModel, FlavorModel

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.properties import ObjectProperty

from kivy.lang import Builder

# Kivy file for Base Screen
Builder.load_file('View/User/BaseScreenKivy.kv')


# //////////////////////////////////////////////////
#                  Screen Classes
# //////////////////////////////////////////////////

class BaseScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty()
    nextButton = ObjectProperty()

    # backButton = ObjectProperty(None)

    # Get ingredient names from database
    # Create buttons dynamically based on the 'cylinder' table
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()

        sqlCount = "SELECT COUNT(id) FROM cylinder;"
        cursor.execute(sqlCount)

        count = cursor.fetchone()

        # print(count)

        sqlBase = "SELECT * FROM cylinder WHERE type='Base';"
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
        for i, base in enumerate(bases):
            button = ToggleButton(text=str(base[1]))
            self.grid.add_widget(button)
            # print("Base " + str(i) + ": " + base[1])

            button.bind(on_press=self.saveButtonName)

    def saveButtonName(self, args):
        # Save the base name in a list to use for the final order
        print("Button clicked")


# //////////////////////////////////////////////////
#                  Screen Manager
# //////////////////////////////////////////////////

# initialize Base Screen manager
# baseScreenManager = ScreenManager()

# initialize Base Screen
baseScreen = BaseScreen(name='Base Screen')


# mainScreen = MainModel.MainScreen(name='Main Screen')
# BaseScreenController.initialize_buttons()

# MainModel.mainScreenManager.add_widget(flavorScreen)
# MainModel.mainScreenManager.add_widget(baseScreen)
# baseScreenManager.add_widget(mainScreen)
# baseScreenManager.transition = CardTransition()
