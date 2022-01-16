import smtplib
from decouple import config


def email_login():
    email, password = config("EMAILID"), config("PASSWORD")
    
    server = smtplib.SMTP('us2.smtp.mailhostbox.com:587')
    server.starttls()
    server.login(email, password)
    
    return (email, server)