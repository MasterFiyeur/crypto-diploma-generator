import requests
import os
from PIL import Image
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

def hide_data_in_png(fileName, firstName, lastName, diploma):
    # Converts user data to a string.
    toHide = strip_accents(firstName.replace(';', '') + ";" + lastName.replace(';', '') + ";" + diploma.replace(';', ''))
    if (len(toHide) > 64):
        raise Exception("Too much data to hide")
    else :
        toHide = toHide + '\0'* (64 - len(toHide))
    # write 64 bytes in file
    f = open("tmp/" + fileName + '.data', "w")
    f.write(toHide)
    f.close()
    
    os.system("openssl ts -query -data tmp/" + fileName + ".data -no_nonce -sha512 -cert -out tmp/" + fileName + ".tsq")
    
    # Get the timestamp signature
    url = "https://freetsa.org/tsr"
    header = {'Content-Type': 'application/timestamp-query'}
    with open('tmp/' + fileName + ".tsq", 'rb') as f:
        requestData = f.read()
    r = requests.post(url, data=requestData, headers=header)
    
    # Removing temporary files
    os.remove("tmp/" + fileName + ".tsq")
    os.remove("tmp/" + fileName + ".data")

    # Final size : 5558 bytes
    # Format : 'firstname;lastname;diploma' (filled by \00 to length 64) then 'timestamp_signature'
    bytes_to_hide = str.encode(toHide) + r.content
    
    # Create image and hide data
    diploma = Image.open(f"tmp/{fileName}.png")
    hide(diploma, bytes_to_hide)
    diploma.save("tmp/" + fileName + ".png")

def vers_8bit(c):
    chaine_binaire = bin(c)[2:]
    return "0"*(8-len(chaine_binaire))+chaine_binaire

def modifier_pixel(pixel, bit):
    # on modifie que la composante rouge
    r_val = pixel[0]
    rep_binaire = bin(r_val)[2:]
    rep_bin_mod = rep_binaire[:-1] + bit
    r_val = int(rep_bin_mod, 2)
    return tuple([r_val] + list(pixel[1:]))

def recuperer_bit_pfaible(pixel):
    r_val = pixel[0]
    return bin(r_val)[-1]

def hide(image,message):
    dimX,dimY = image.size
    im = image.load()
    message_binaire = ''.join([vers_8bit(c) for c in message])
    posx_pixel = 0
    posy_pixel = 0
    for bit in message_binaire:
        im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
        posx_pixel += 1
        if (posx_pixel == dimX):
            posx_pixel = 0
            posy_pixel += 1
        assert(posy_pixel < dimY)

def recover(image, taille):
    message = b''
    dimX,dimY = image.size
    im = image.load()
    posx_pixel = 0
    posy_pixel = 0
    for rang_car in range(0,taille):
        rep_binaire = ""
        for rang_bit in range(0,8):
            rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
            posx_pixel +=1
            if (posx_pixel == dimX):
                posx_pixel = 0
                posy_pixel += 1
        message += int(rep_binaire, 2).to_bytes(1,'big')
    return message

def recover_data_from_png(fileName):
    length = 5558
    image = Image.open('tmp/' + fileName + '.png')
    message = recover(image, length)
    data = message[:64].decode("utf-8").split(';')
    
    file = open("tmp/" + fileName + ".ts", "wb")
    file.write(message[64:])
    file.close
    file = open("tmp/" + fileName + ".data", "wb")
    file.write(message[:64])
    file.close
    return data[0], data[1], data[2].rstrip('\x00')

def verify_ts(fileName):
    os.system("openssl ts -verify -in tmp/" + fileName + ".ts -CAfile resources/cacert.pem -untrusted resources/tsa.crt -data tmp/" + fileName + ".data > tmp/" + fileName + ".tsv")
    verification = open("tmp/" + fileName + ".tsv", "r").read().find("Verification: OK") != -1
    if verification:
        os.system("openssl ts -reply -in tmp/" + fileName + ".ts -text -out tmp/" + fileName + ".timestamp")
        timestamp = open("tmp/" + fileName + ".timestamp", "r").read()
        timestamp = timestamp[timestamp.find('Time stamp: ')+12:timestamp.find('GMT')+3]
    else:
        timestamp = "Invalid"
    os.system('rm tmp/' + fileName + '*')
    return verification, timestamp
