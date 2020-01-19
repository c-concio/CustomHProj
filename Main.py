from Model import AdminModel
from Controller import AdminMainScreenController
import kivy

kivy.require('1.11.1')

from kivy.app import App


class MainApp(App):

    def build(self):
        screenManager = AdminModel.screenManager
        AdminModel.adminMainScreen.initialize_buttons()
        AdminModel.inventoryScreen.add_template()
        AdminModel.inventoryScreen.add_template()
        AdminModel.inventoryScreen.add_template()
        AdminModel.inventoryScreen.add_template()
        return screenManager

if __name__ == '__main__':
    MainApp().run()
