import sqlite3

import kivy
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton

from Model import MainModel

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.properties import ObjectProperty

from kivy.lang import Builder

# Kivy file for Base Screen
Builder.load_file('View/User/FlavorScreenKivy.kv')


# //////////////////////////////////////////////////
#                  Screen Classes
# //////////////////////////////////////////////////

class FlavorScreen(Screen):
    # grid object from kivy file
    grid = ObjectProperty()
    nextButton = ObjectProperty()
    # backButton = ObjectProperty(None)

    # Get ingredient names from database
    # Create buttons dynamically based on the 'cylinder' table
    def __init__(self, **kwargs):
        super(FlavorScreen, self).__init__(**kwargs)
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()

        sqlBase = "SELECT * FROM cylinder WHERE type='Flavor';"
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


flavorScreen = FlavorScreen(name='Flavor Screen')

# MainModel.mainScreenManager.add_widget(flavorScreen)
