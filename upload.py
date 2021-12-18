from flask import Flask, jsonify, request
from decouple import config
from .email_login import login
from .database import db_uploader, get_mongodb


db_uploader = db_uploader()
mongo_db = get_mongodb()
app = Flask(__name__)


@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
	certificate, sheet = request.files['certificate'], request.files['sheet']
	session_id = mongo_db.insert_one({}).inserted_id

	certificate_response = db_uploader(certificate, public_id = f"data/{session_id}/certificate")
	sheet_response = db_uploader(sheet, public_id = f"data/{session_id}/sheet")

	mongo_db.data.update_one({
		{"_id": session_id}, 
		{"$set": {
			"certificate": certificate_response["secure_url"],
			"sheet": sheet_response["secure_url"],
		}}	
	})
	
	return jsonify({
		"certificate_url": certificate_response["secure_url"], 
		"session_id": session_id
		})


if __name__ == '__main__':
	app.run(debug = True)
