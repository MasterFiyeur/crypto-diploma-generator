import smtplib
from etc.settings import CONFIG # Settings
import os

mailserver = smtplib.SMTP(CONFIG['SMTP']['SERVER'], CONFIG['SMTP']['PORT'])
mailserver.starttls()
mailserver.login(CONFIG['SMTP']['USERNAME'], CONFIG['SMTP']['PASSWORD'])
mailserver.set_debuglevel(1)


def send_mail():
    pass
    # send the mail