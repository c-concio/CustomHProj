from Model import AdminModel
from Controller import AdminMainScreenController, DatabaseController
from Model import UserModel
from Controller import UserController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

    def build(self):
        screenManager = AdminModel.screenManager
        AdminMainScreenController.setup_inventory_screen()
        screenManager = UserModel.screenManager
        return screenManager


if __name__ == '__main__':
    MainApp().run()
    DatabaseController.database_close()
