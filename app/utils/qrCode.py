import qrcode
import PIL
import io
from flask import send_file


def makeQRCode(targetLink):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(targetLink)
    qr.make(fit=True)
    img = qr.make_image()
    return imgFile(img)


def imgFile(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', cache_timeout=0)
