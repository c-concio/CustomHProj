from Model import AdminModel
from Controller import AdminMainScreenController, DatabaseController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

    def build(self):
        screen_manager = AdminModel.screenManager
        AdminMainScreenController.initialize_screen_manager()
        AdminMainScreenController.setup_inventory_screen()
        return screen_manager


if __name__ == '__main__':
    MainApp().run()
    DatabaseController.database_close()
