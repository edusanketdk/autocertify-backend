from PIL import Image, ImageFont, ImageDraw
import pandas as pd
from .database import get_mongodb
from urllib.request import urlopen
from io import BytesIO
import requests
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email_login import email_login
import os



def process(data):
    mongo_db = get_mongodb()
    sender_email, email_server = email_login()
    session_id = data["session_id"]

    document = mongo_db.find({"_id": session_id}).limit(1)
    certificate, sheet = document["certificate"], document["sheet"]

    certificate = Image.open(urlopen(certificate))
    sheet = read_sheet(sheet)

    location = data["location"]
    font = ImageFont.truetype(BytesIO(requests.get(data["font"]["family"]).content), data["font"]["size"])

    for person in sheet:
        created_certificate = create_certificate(person["name"], certificate, location, font)
        send_certificate(person["name"], person["email"], created_certificate, email_server, data["email"], sender_email)



def create_certificate(name, img, location, font):
    draw = ImageDraw.Draw(img)

    W, H = location
    w, h = draw.textsize(str(name), font=font)
    draw.text(((W - w) / 2, (H - h) / 2), name, (0, 0, 0), font=font)

    rgb = Image.new('RGB', img.size)
    rgb.paste(img)

    return rgb.tobytes()



def read_sheet(sheet):
    return pd.read_excel(sheet)



def send_certificate(email, certificate, server, email_data, sender_email):
    msg = MIMEMultipart()
    msg['Subject'] = email_data["subject"]
    msg['From'] = sender_email
    msg['To'] = email

    msg.preamble = 'Multipart massage.\n'

    body = email_data["body"]
    part = MIMEText(body)
    msg.attach(part)

    part = MIMEApplication(certificate)
    part.add_header('Content-Disposition', 'attachment', filename=f"certificate.jpg")
    msg.attach(part)

    server.sendmail(msg['From'], msg['To'], msg.as_string())