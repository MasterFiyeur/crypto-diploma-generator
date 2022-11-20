import base64
import OpenSSL
from etc.settings import CONFIG # Settings



def signCertificate(data): 
    
    passphrase = CONFIG['CA_PASSPHRASE']['SERVER']
    passphrase = bytes(passphrase, 'utf-8')
    privKeyPath = open("CA/private/serveur.key").read() 
    privKey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, privKeyPath, passphrase) 
    sign = OpenSSL.crypto.sign(privKey, data, "sha256") 
    return sign 
 
def verifySignature(data, sign): 
    certPath = open("CA/certs/serveur.pem").read() 
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certPath) 
    verif = OpenSSL.crypto.verify(cert, sign, data, 'sha256')
    return verif