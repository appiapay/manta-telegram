import qrcode
import os
from PIL import Image


# generate QRCode with logo image
def make_logo_qr(msg: str, logo: str, output):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )

    # add string to transform
    qr.add_data(msg)

    qr.make(fit=True)
    # generate QRCode
    img = qr.make_image()

    img = img.convert("RGBA")

    # add logo
    if logo and os.path.exists(logo):
        icon = Image.open(logo)
        # get size of QRCode image
        img_w, img_h = img.size

        factor = 3
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        # size of logo <= 1/4 * QRCode image
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        # see http://pillow.readthedocs.org/handbook/tutorial.html

        # compute the position of logo in output image
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        # paste logo on the output image
        img.paste(icon, (w, h), icon)
        # see：http://pillow.readthedocs.org/reference/Image.html#PIL.Image.Image.paste

    # save QRCode image
    img.save(output, format='png')
