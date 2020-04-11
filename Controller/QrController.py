import qrcode
from kivy.properties import ObjectProperty

from Controller import DatabaseController, MainScreenController
from Model import QrModel


def initialize_qr_buttons():
    QrModel.qrScreen.backButton.bind(on_press=lambda x: MainScreenController.return_screen('User Main Screen'))


def generateQrCode():
    # get from the database the information from the temporary database and compile it into one string
    string = DatabaseController.get_cylinder_ingredients()

    qr = qrcode.QRCode(
        version= 1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=2
    )

    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image()

    img.save("./Images/qr.png")