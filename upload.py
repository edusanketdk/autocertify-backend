from flask import Flask, jsonify, request
from decouple import config
from .login import login
from .database import db_uploader, get_mongodb


db_uploader = db_uploader()
mongo_db = get_mongodb()
app = Flask(__name__)


@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
	certificate, sheet = request.files['certificate'], request.files['sheet']
	session_id = request.meta["session_id"]

	certificate_response = db_uploader(certificate)
	sheet_response = db_uploader(sheet)

	mongo_db.data.insert_one({
		"_id": session_id,
		"certificate": certificate_response["secure_url"],
		"sheet": sheet_response["secure_url"],
	})
	
	return jsonify({"url": certificate_response["secure_url"]})


if __name__ == '__main__':
	app.run(debug = True)
