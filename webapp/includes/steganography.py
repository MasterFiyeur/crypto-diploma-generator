import uuid
import requests
import base64
import os

def user_data_to_string(firstName, lastName, diploma):
    # Converts user data to a string.
    toHide = firstName.replace(';', '') + ";" + lastName.replace(';', '') + ";" + diploma.replace(';', '')
    fileName = str(uuid.uuid4())
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
    
    # Format : 'firstname;lastname;diploma' (filled by \00 to length 64) then 'timestamp_signature'
    return str.encode(toHide) + r.content