from kivy.uix.screenmanager import ScreenManager

from Model import AdminModel, MainModel
from Controller import AdminMainScreenController, DatabaseController
from Model import UserModel
from Controller import UserController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

    def build(self):
        # screenManager = AdminModel.screenManager
        screenManager = MainModel.mainScreenManager
        AdminMainScreenController.setup_inventory_screen()
        # screenManager = UserModel.screenManager

        # testScreenManager = ScreenManager();
        # splitScreen = UserModel.TestSplitScreen()
        # #splitScreen.carouselWidget.add_widget(UserModel.AmountScreen())


        # testScreenManager.add_widget(splitScreen)

        return screenManager


if __name__ == '__main__':
    MainApp().run()
    DatabaseController.database_close()