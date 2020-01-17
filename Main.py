from Model import ScreenManager
from Model import AdminScreens
from Controller import AdminMainScreenController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

    def build(self):
        screenManager = ScreenManager.screenManager
        ScreenManager.adminMainScreen.initialize_buttons()
        return screenManager


if __name__ == '__main__':
    MainApp().run()
