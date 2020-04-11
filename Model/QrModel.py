import kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from Controller import QrController, MainScreenController, DatabaseController

kivy.require('1.11.1')
Builder.load_file('View/User/QrScreenKivy.kv')


class QrScreen(Screen):
    titleLabel = ObjectProperty(None)
    img = ObjectProperty(None)
    backButton = ObjectProperty(None)
    userString = ""
    baseArray = []
    flavorArray = []
    sauceSize = ""

    def __init__(self, **kwargs):
        super(QrScreen, self).__init__(**kwargs)

        # self.titleLabel.height = Window.height * 0.15
        # if (Window.height > Window.width):
        #     self.titleLabel.height = Window.height * 0.1
        # else:
        #     self.titleLabel.height = Window.height * 0.15


        # if (Window.height > Window.width):
        #     self.img.size = (Window.width * 0.9, Window.width* 0.9)
        # else:
        #     self.img.size = (Window.height * 0.75, Window.height * 0.75)

    def on_enter(self, *args):
        QrController.generateQrCode()

        self.img.source = "./Images/qr.png"
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.userString = ""

    def on_leave(self, *args):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    # terminate when the key "]" is entered
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.userString += keycode[1]

        if keycode[1] == "]":
            # if the ] is found the qr code, parse the string and save information into the temporary database
            stringArray = self.userString.split("//")
            # print("String size: " + stringArray.__sizeof__())

            # Size//Medium//Bases//Ketchup//Flavor//Cajun
            for i in range(0, stringArray.__len__()):
                if stringArray[i] == "size":
                    i += 1
                    self.sauceSize = stringArray[i]
                    i += 1

                elif stringArray[i] == "bases":
                    i += 1
                    while stringArray[i] != "flavor":
                        self.baseArray.append(stringArray[i])
                        i += 1
                elif stringArray[i] == "flavor":
                    while i < stringArray.__len__() - 1:
                        i += 1
                        if stringArray[i] == "]":
                            continue
                        self.flavorArray.append(stringArray[i])

            # clear the temporary database then add the new recipes from the QR code
            DatabaseController.add_temporary_recipe(self.baseArray, self.flavorArray)


qrScreen = QrScreen(name="QR Screen")
QrController.initialize_qr_buttons()
