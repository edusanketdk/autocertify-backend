import smtplib
from decouple import config


def email_login():
    email, password = config(EMAILID), config(PASSWORD)
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(email, password)
    
    return (email, server)