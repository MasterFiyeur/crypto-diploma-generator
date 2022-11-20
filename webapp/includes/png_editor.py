from PIL import Image, ImageDraw, ImageFont
import os
import qrcode
import glob
import cv2
import pandas as pd
import pathlib
from includes.cryptog import *


DIR = os.getcwd()

NAME_FONT = ImageFont.truetype(os.path.join(DIR,'resources/FiraCode.ttf'), 80)
FORMATION_FONT = ImageFont.truetype(os.path.join(DIR,'resources/FiraCode.ttf'), 120)
FONT_COLOR = (0, 0, 0)

def draw_data(name, firstname, formation):
    img = Image.open(os.path.join(DIR,f'resources/diploma-template.png'))
    W, H = img.size
    draw = ImageDraw.Draw(img)
    names = f'{firstname.lower().capitalize()} {name.upper()}'
    _, _, w, h = draw.textbbox((0, 0), names, font=NAME_FONT)
    _, _, w2, h2 = draw.textbbox((0, 0), formation, font=FORMATION_FONT)
    draw.text(((W-w)/2, (H-h)/2-50), names, font=NAME_FONT, fill=FONT_COLOR)
    draw.text(((W-w2)/2, (H-h2)/2+75), formation, font=FORMATION_FONT, fill=FONT_COLOR)
    return img


def draw_qrcode(data, img):
    position = (1417,931)
    myQrcode = qrcode.QRCode(
        version = 1,
        border = 3,
        box_size = 3,
    )
    
    myQrcode.add_data(data)
    myQrcode.make(fit=True)
    myQrcode_img = myQrcode.make_image(fill_color="black", back_color="white")
    
    img.paste(myQrcode_img, position)
    return img
   
        
def generate_diploma(name, firstname, formation, uuid):
    
    data = firstname.replace(';', '') + ";" + name.replace(';', '') + ";" + formation.replace(';', '')
    if (len(data) > 64):
        raise Exception("Too much data to hide")
    else :
        data = data + '\0'* (64 - len(data))

    signed_data = signCertificate(data)
    signed_data = base64.b64encode(signed_data)
        
    img = draw_data(name, firstname, formation)
    img = draw_qrcode(signed_data, img)
    
    img.save(os.path.join(DIR,f'tmp/{uuid}.png'))
    
    return img  
        
        
def verify_signature(fileName, firstname, lastname, diploma):
    data = data = firstname.replace(';', '') + ";" + lastname.replace(';', '') + ";" + diploma.replace(';', '')
    if (len(data) > 64):
        raise Exception("Too much data to hide")
    else :
        data = data + '\0'* (64 - len(data))
    
    im = Image.open(os.path.join('tmp', fileName + '.png'))

    width, height = im.size

    left = 1418
    top = 3 * height / 4 + 2
    right = width - 100
    bottom = height - 75

    im1 = im.crop((left, top, right, bottom))

    im1.save('tmp/qrcode.png')

    img = cv2.imread('tmp/qrcode.png')
    detect = cv2.QRCodeDetector()
    value, points, _ = detect.detectAndDecode(img)
    signature = base64.b64decode(value)
    verif = verifySignature(data, signature)
    
    if verif == None:
        return True
    else:
        return False
