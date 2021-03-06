from database import get_db_uploader, get_mongodb
from flask import Flask, jsonify, request
from mark_stage import mark_stage
from flask_cors import CORS
import logging



def create_app():
	db_uploader = get_db_uploader()
	mongo_db = get_mongodb()

	app = Flask(__name__)
	app.config['CORS_HEADERS'] = 'Content-Type'
	CORS(app, resources={r"/": {"origins": "*"}})
	

	@app.route('/', methods=['POST'])
	def upload():
		certificate, sheet = request.files['certificate'], request.files['sheet']
		session_id = mongo_db.data.insert_one({}).inserted_id

		mark_stage(session_id, 'upload')

		certificate_response = db_uploader(certificate, public_id=f"data/{session_id}/certificate", resource_type="auto")
		sheet_response = db_uploader(sheet, public_id=f"data/{session_id}/sheet", resource_type="auto")

		mongo_db.data.update_one({
			"_id": session_id
		}, {
			"$set": {
				"certificate": certificate_response["secure_url"],
				"sheet": sheet_response["secure_url"],
			}
		})

		response = jsonify({
			"certificate_url": certificate_response["secure_url"],
			"certificate_width": certificate_response["width"],
			"certificate_height": certificate_response["height"],
			"session_id": str(session_id)
		})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response


	@app.errorhandler(500)
	def server_error(e):
		logging.exception('An error occurred during a request. %s', e)
		return "An internal error occured", 500


	return app
