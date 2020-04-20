import sqlite3

import kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
import time

kivy.require('1.11.1')

from kivy.app import App

Builder.load_file("Simulation.kv")


class SimulationScreen(Screen):
    box = ObjectProperty(None)
    baseRow = ObjectProperty(None)
    flavorRow = ObjectProperty(None)


class SimulationCylinderTemplate(GridLayout):
    widget = ObjectProperty(None)
    bar = ObjectProperty(None)
    name = ObjectProperty(None)
    ingredient = ObjectProperty(None)
    steps = ObjectProperty(None)

    maxValue = 0
    value = 0

    def __init__(self, maxValue):
        super().__init__()
        self.maxValue = maxValue

    def setAmount(self, value):
        self.value = value
        self.bar.amount = value/self.maxValue
        self.steps.text = str(value)

    def setName(self, newName):
        self.name.text = newName

    def setIngredient(self, newIngredient):
        self.ingredient.text = newIngredient

    def getAmount(self):
        return self.steps.text

    def getName(self):
        return self.name.text

    def getIngredient(self):
        return self.ingredient.text


class MainApp(App):

    cylinderTemplates = []
    conn = sqlite3.connect(r'database/pysqlite.db')
    cursor = conn.cursor()

    def build(self):

        Window.size = (1400, 700)
        screenManager = ScreenManager()
        simulationScreen = SimulationScreen()

        # get all the base ingredients and save the ingredient, cylinder name, and amount


        self.cursor.execute("SELECT id, ingredient, steps, type FROM cylinder")
        results = self.cursor.fetchall()

        for result in results:
            newTemplate = SimulationCylinderTemplate(100)
            newTemplate.setName("Cylinder " + str(result[0]))
            newTemplate.setIngredient(result[1])
            newTemplate.setAmount(result[2])
            self.cylinderTemplates.append(newTemplate)
            if result[3] == 'base':
                simulationScreen.baseRow.add_widget(newTemplate)
            else:
                simulationScreen.flavorRow.add_widget(newTemplate)

        screenManager.add_widget(simulationScreen)

        event = Clock.schedule_interval(self.callIt, 1)
        return screenManager

    def callIt(self, dt):
        self.cursor.execute("SELECT id, ingredient, steps, type FROM cylinder")
        results = self.cursor.fetchall()

        counter = 0
        for result in results:
            if self.cylinderTemplates[counter].getIngredient() != result[1]:
                self.cylinderTemplates[counter].setIngredient(result[1])
            if self.cylinderTemplates[counter].getAmount != result[2]:
                self.cylinderTemplates[counter].setAmount(result[2])

            counter += 1


if __name__ == '__main__':
    MainApp().run()