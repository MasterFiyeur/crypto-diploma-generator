import base64
import OpenSSL
from etc.settings import CONFIG # Settings



def signWithCertificate(data): 
    
    passphrase = CONFIG['CA_PASSPHRASE']['SERVER']
    passphrase = bytes(passphrase, 'utf-8')
    privateKey = open("CA/private/serveur.key").read() 
    PKey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, privateKey, passphrase) 
    sign = OpenSSL.crypto.sign(PKey, data, "sha256") 
    return sign 
 
def verifySignature(data, sign): 
    rawCert = open("CA/certs/serveur.pem").read() 
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, rawCert) 
    verification = OpenSSL.crypto.verify(cert, sign, data, 'sha256') 
    return verification