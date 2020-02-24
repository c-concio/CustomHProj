import kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from Controller import QrController

kivy.require('1.11.1')
Builder.load_file('View/User/QrScreenKivy.kv')

class QrScreen(Screen):
    titleLabel = ObjectProperty(None)
    img = ObjectProperty(None)

    def __init__(self, name):
        super().__init__()

        self.titleLabel.height = Window.height * 0.15
        if (Window.height > Window.width):
            self.titleLabel.height = Window.height * 0.1
        else:
            self.titleLabel.height = Window.height * 0.15

        QrController.generateQrCode()

        self.img.source = "./Images/qr.png"
        if (Window.height > Window.width):
            self.img.size = (Window.width * 0.9, Window.width* 0.9)
        else:
            self.img.size = (Window.height * 0.75, Window.height * 0.75)