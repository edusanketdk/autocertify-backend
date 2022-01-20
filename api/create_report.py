from email.message import EmailMessage
from email_login import email_login



def create_report(email):
	sender_email, email_server = email_login()

	msg = EmailMessage()

	msg['From'] = sender_email
	msg['To'] = email
	msg['Subject'] = "AutoCertify completed your task!"

	body = "Hi,\n\nHope this email finds you in good health. We would like to let you know that all the certificates have been sent via mails, using the awesome AutoCertify.\n\nThanks for using AutoCertify :)\n\n-AutoCertify"
	msg.set_content(body)
	
	email_server.sendmail(msg['From'], msg['To'], msg.as_string())