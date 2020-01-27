from kivy.app import App
from CustomHProj.Model import UserModel
from CustomHProj.Controller import UserController
import kivy

kivy.require('1.11.1')  # replace with your current kivy version !


class MainApp(App):
    def build(self):
        screenManager = UserModel.screenManager
        return screenManager


if __name__ == '__main__':
    MainApp().run()
