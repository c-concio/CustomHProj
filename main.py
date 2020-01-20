import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase

kivy.require('1.9.0')  # replace with your current kivy version !

LabelBase.register(name="Pacifico", fn_regular="Pacifico.ttf")
LabelBase.register(name="OstrichSans", fn_regular="ostrich-regular.ttf")


# orange = [0.059,0.969 ,0.961 ,1.0]


class HomeScreen(Screen):
    def startBtn(self):
        sm.current = "size"


class SizeScreen(Screen):
    def startBtn(self):
        sm.current = "base"


class BaseScreen(Screen):
    def SauceMonthBtn(self):
        sm.current = "sauceMonth"

    def startBtn(self):
        sm.current = "flavour"


class FlavourScreen(Screen):
    pass


class SauceOfMonth(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("proj.kv")

sm = WindowManager()

screens = [HomeScreen(name="Home"), SizeScreen(name="size"), BaseScreen(name="base"),SauceOfMonth(name="sauceMonth"), FlavourScreen(name="flavour") ]
for screen in screens:
    sm.add_widget(screen)


class MyProject(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyProject().run()
