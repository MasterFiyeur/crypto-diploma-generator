import smtplib
from etc.settings import CONFIG # Settings
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

mailserver = smtplib.SMTP(CONFIG['SMTP']['SERVER'], CONFIG['SMTP']['PORT'])
mailserver.starttls()
mailserver.login(CONFIG['SMTP']['USERNAME'], CONFIG['SMTP']['PASSWORD'])
mailserver.set_debuglevel(1)


def send_mail():
    # msg = MIMEMultipart()
    # msg['From'] = CONFIG['SMTP']['USERNAME']
    # msg['To'] = "julientheo@cy-tech.fr"
    # msg['Subject'] = 'hello world from smtp server'


    # msg_content = MIMEText('send with attachment...', 'plain', 'utf-8')
    # msg.attach(msg_content)
    
    # with open('test.png', 'rb') as f:
    #     # set attachment mime and file name, the image type is png
    #     mime = MIMEBase('image', 'png', filename='img1.png')
    #     # add required header data:
    #     mime.add_header('Content-Disposition', 'attachment', filename='img1.png')
    #     mime.add_header('X-Attachment-Id', '0')
    #     mime.add_header('Content-ID', '<0>')
    #     # read attachment file content into the MIMEBase object
    #     mime.set_payload(f.read())
    #     # encode with base64
    #     encode_base64(mime)
    #     # add MIMEBase object to MIMEMultipart object
    #     msg.attach(mime)
    
    # file = open('test.txt', 'w')
    # file.write(msg.as_string())
    # file.close()
    file = open('test_courrier.txt', 'r')
    msg = file.read()
    file.close()
    mailserver.sendmail(CONFIG['SMTP']['USERNAME'], 'theo.julien@cy-tech.fr', msg)