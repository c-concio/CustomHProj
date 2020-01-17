from View.Admin import screens
import kivy
kivy.require('1.11.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

# make the app fullscreen
Window.fullscreen = 'auto'

# use the kv definitions found in the adminScreens.kv file
Builder.load_file('View/Admin/adminScreens.kv')

# initialize Screen manager
screenManager = ScreenManager()
screenManager.add_widget(screens.AdminMainScreen(name='Admin Page'))

class MainApp(App):

    def build(self):
        return screenManager


if __name__ == '__main__':
    MainApp().run()
