import smtplib
from decouple import config


def email_login():
    email, password = config("EMAILID"), config("PASSWORD")
    
    server = smtplib.SMTP('smtp.autocertify.tech:587')
    server.starttls()
    server.login(email, password)
    
    return (email, server)