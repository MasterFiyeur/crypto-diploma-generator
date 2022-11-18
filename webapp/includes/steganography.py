import requests
import os
from PIL import Image

def hide_data_in_png(fileName, firstName, lastName, diploma):
    # Converts user data to a string.
    toHide = firstName.replace(';', '') + ";" + lastName.replace(';', '') + ";" + diploma.replace(';', '')
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