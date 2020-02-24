import qrcode

from Controller import DatabaseController


def generateQrCode():
    # get from the database the information from the temporary database and compile it into one string
    string = DatabaseController.get_temporary_table()

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