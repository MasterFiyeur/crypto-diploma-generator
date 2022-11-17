from PIL import Image, ImageDraw, ImageFont
import os
import qrcode
import pyqrcodeng as pyqrcode


DIR = os.getcwd()

NAME_FONT = ImageFont.truetype(os.path.join(DIR,'resources/FiraCode.ttf'), 80)
FORMATION_FONT = ImageFont.truetype(os.path.join(DIR,'resources/FiraCode.ttf'), 120)
FONT_COLOR = (0, 0, 0)

def draw_data(name, firstname, formation, filename):
    img = Image.open(os.path.join(DIR,'resources/diploma-template.png'))
    W, H = img.size
    img = Image.open(os.path.join(DIR,'resources/diploma-template.png'))
    draw = ImageDraw.Draw(img)
    names = f'{name.upper()} {firstname.lower().capitalize()}'
    _, _, w, h = draw.textbbox((0, 0), names, font=NAME_FONT)
    _, _, w2, h2 = draw.textbbox((0, 0), formation, font=FORMATION_FONT)
    draw.text(((W-w)/2, (H-h)/2-50), names, font=NAME_FONT, fill=FONT_COLOR)
    draw.text(((W-w2)/2, (H-h2)/2+75), formation, font=FORMATION_FONT, fill=FONT_COLOR)
    img.save(os.path.join(DIR,f'tmp/{filename}.png'))
    return img



def draw_qrcode(img, filename):
    
    f = open(f'tmp/{filename}.data', 'rb')
    data = f.read()
    
    print(data)
    
    # os.system(f'openssl dgst -sign {DIR}/CA/private/serveur.key -keyform PEM -sha256 -out tmp/{filename}.data.sign -binary "{data}"')
    
    # position = (1417,931)
    # myQrcode = qrcode.QRCode(
    #     version = 1,
    #     border = 0,
    # )
    
    # myQrcode.add_data(b'a')
    # myQrcode.make()
    # myQrcode_img = myQrcode.make_image(fill_color="black", back_color="white")
    

    # myQrcode_img.save(os.path.join(DIR,f'tmp/qrcode_test.png'))
    
    
    # img.paste(myQrcode_img, position)
    # img.save(os.path.join(DIR,f'tmp/{filename}.png'))
    # f.close()
    # img.show()




# myName = 'Name'
# MyFirstName = 'Firstname'
# myFormation = 'Formation'
# data= b'0010\x00'
# myImage = draw_data(myName, MyFirstName, myFormation)
# myQRcode = draw_qrcode(data, myImage)




