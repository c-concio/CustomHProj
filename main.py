from kivy.core.window import Window

from Model import AdminModel, MainModel
from Controller import AdminMainScreenController, DatabaseController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

    def build(self):
        # screenManager = AdminModel.screenManager
        screenManager = MainModel.mainScreenManager
        AdminMainScreenController.setup_inventory_screen()
        return screenManager


if __name__ == '__main__':
    MainApp().run()
    DatabaseController.database_close()