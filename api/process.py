from PIL import Image, ImageFont, ImageDraw
from email.message import EmailMessage
from email_login import email_login
from urllib.request import urlopen
from database import get_mongodb
from bson import ObjectId
from copy import deepcopy
from io import BytesIO
import pandas as pd
import requests



def process(data):
    mongo_db = get_mongodb()
    sender_email, email_server = email_login()
    session_id = data["session_id"]

    document = mongo_db.data.find_one({"_id": ObjectId(session_id)})
    certificate, sheet = document["certificate"], document["sheet"]

    certificate = Image.open(urlopen(certificate))
    sheet = read_sheet(sheet)

    location = data["location"]
    font = ImageFont.truetype(BytesIO(requests.get(data["font"]["family"]).content), data["font"]["size"])

    for i, person in sheet.iterrows():
        created_certificate = create_certificate(person["name"], deepcopy(certificate), location, font)
        send_certificate(person["email"], created_certificate, email_server, data["email"], sender_email)



def create_certificate(name, img, location, font):
    draw = ImageDraw.Draw(img)
    name = name.title()

    W, H = location["width"], location["height"]
    w, h = draw.textsize(str(name), font=font)
    draw.text((W - w/2, H - h/2), name, (0, 0, 0), font=font)

    rgb = Image.new('RGB', img.size)
    rgb.paste(img)
	
    img_io = BytesIO()
    rgb.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)

    return img_io



def read_sheet(sheet):
    sheet = pd.read_excel(sheet)
    sheet.columns = [i.lower() for i in sheet.columns]
    return sheet



def send_certificate(email, certificate, server, email_data, sender_email):
	msg = EmailMessage()

	msg['From'] = sender_email
	msg['To'] = email
	msg['Subject'] = email_data["subject"]

	body = email_data["body"]
	msg.set_content(body)
	mime_type, mime_subtype = "image", "jpeg"

	msg.add_attachment(
		certificate.read(),
		maintype=mime_type,
		subtype=mime_subtype,
		filename='certificate.jpg',
		)
	
	server.sendmail(msg['From'], msg['To'], msg.as_string())

