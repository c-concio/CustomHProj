from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from Model import AdminModel, MainModel, QrModel
from Controller import AdminMainScreenController, DatabaseController
from Model import UserModel
from Controller import UserController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

# TODO: Dynamic flavor buttons and number of bases for the AmountScreen

    def build(self):
        # screenManager = AdminModel.screenManager
        screenManager = MainModel.mainScreenManager
        # AdminMainScreenController.setup_inventory_screen()
        # screenManager = UserModel.screenManager

        # iPhone screen size
        # Window.size = (320, 540)

        # iPhone XR screen size
        Window.size = (414, 896)

        # Nexus 9
        # Window.size = (768, 1024)

        # FullScreen
        # Window.fullscreen = True

        self.headerFont = UserController.header_font_size()


        testScreenManager = ScreenManager();


        testScreenManager.add_widget(QrModel.QrScreen(name="Qr"))

        return screenManager


if __name__ == '__main__':
    MainApp().run()
    DatabaseController.database_close()