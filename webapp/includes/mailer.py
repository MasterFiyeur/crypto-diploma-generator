import smtplib
from etc.settings import CONFIG # Settings
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os

mailserver = smtplib.SMTP(CONFIG['SMTP']['SERVER'], CONFIG['SMTP']['PORT'])
mailserver.starttls()
mailserver.login(CONFIG['SMTP']['USERNAME'], CONFIG['SMTP']['PASSWORD'])
mailserver.set_debuglevel(1)

PUBLIC_KEY_PATH = 'CA/certs/email.pem' 
PRIVATE_KEY_PATH = 'CA/private/email.key'
MSG_FROM = CONFIG['SMTP']['USERNAME']
MSG_SUBJECT = 'Your diploma has just been created'
MSG_CONTENT = """
Hello,

Congratulations, you have just received your diploma.
You will find it attached.

Sincerely
"""
MSG_PNG_NAME = 'diploma.png'


def send_mail(fileName, email):
    # Create the message
    msg = MIMEMultipart()
    msg['From'] = MSG_FROM
    msg['To'] = email
    msg['Subject'] = MSG_SUBJECT

    # Add the body
    msg_content = MIMEText(MSG_CONTENT, 'plain', 'utf-8')
    msg.attach(msg_content)
    
    # Add the attachment (diploma)
    with open("tmp/" + fileName + "", 'rb') as f:
        mime = MIMEBase('image', 'png', filename=MSG_PNG_NAME)
        mime.add_header('Content-Disposition', 'attachment', filename=MSG_PNG_NAME)
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        mime.set_payload(f.read())
        encode_base64(mime)
        msg.attach(mime)
    
    # Create the S/MIME format
    file = open( 'tmp/' + fileName + '.txt', 'w')
    file.write(msg.as_string())
    file.close()
    # os.system('openssl smime -signer ' + PUBLIC_KEY_PATH + ' -from "' + MSG_FROM + '" -to "' + email + '" -subject "' + MSG_SUBJECT + '" -sign -inkey ' + PRIVATE_KEY_PATH +' -in tmp/' + fileName + '.txt -out tmp/' + fileName + '.txt -passin pass:'+ CONFIG['CA_PASSPHRASE']['EMAIL'])
    
    # file = open( 'tmp/' + fileName + '.txt', 'r')
    # msg = file.read()
    # file.close()
    # mailserver.sendmail(CONFIG['SMTP']['USERNAME'], 'theo.julien@cy-tech.fr', msg)