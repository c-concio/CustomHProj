import sqlite3

from kivy.uix.button import Button

from Controller import AdminMainScreenController, MainScreenController, BaseScreenController
import kivy

from Model import MainModel

kivy.require('1.11.1')  # replace with your current kivy version !
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.properties import ObjectProperty

from kivy.lang import Builder

# Kivy file for Base Screen
Builder.load_file('View/BaseScreenKivy.kv')


# //////////////////////////////////////////////////
#                  Screen Classes
# //////////////////////////////////////////////////

class BaseScreen(Screen):
    # backButton = ObjectProperty(None)

    # Get ingredient names from database
    # Create buttons dynamically based on the 'cylinder' table
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        connect = sqlite3.connect(r"database/pysqlite.db")
        cursor = connect.cursor()

        sqlCount = "SELECT COUNT(id) FROM cylinder;"
        cursor.execute(sqlCount)

        count = cursor.fetchone()

        print(count)

        sqlBase = "SELECT * FROM cylinder;"
        cursor.execute(sqlBase)
        bases = cursor.fetchall()

        cursor.close()

        # Dynamic buttons
        for i, base in enumerate(bases):
            x_pos_hint = .2
            y_pos_hint = .8
            j = 0
            if(i >= 3):
                x_pos_hint = .4
                y_pos_hint = .8
                j = 0
            button = Button(text=str(base[1]), size_hint=(.1, .1), pos_hint={'x': x_pos_hint, 'y': y_pos_hint - j/5})
            print(j/5)
            j += 1
            self.add_widget(button)
            print("Base " + str(i) + ": " + base[1])

            button.bind(on_press=self.saveButtonName)

    @staticmethod
    def saveButtonName(self):
        # Save the base name in a list to use for the final order
        print("Button clicked")


# //////////////////////////////////////////////////
#                  Screen Manager
# //////////////////////////////////////////////////

# initialize Base Screen manager
baseScreenManager = ScreenManager()

# initialize Base Screen
baseScreen = BaseScreen(name='Base Screen')
# mainScreen = MainModel.MainScreen(name='Main Screen')

# BaseScreenController.initialize_buttons()

# MainModel.mainScreenManager.add_widget(baseScreen)
# baseScreenManager.add_widget(mainScreen)
# baseScreenManager.transition = CardTransition()
