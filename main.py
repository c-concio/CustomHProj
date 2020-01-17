from Model import screenManager
import kivy
kivy.require('1.11.1')

from kivy.app import App

class MainApp(App):

    def build(self):
        return screenManager.ScreenManager.sm

if __name__ == '__main__':
    MainApp().run()
