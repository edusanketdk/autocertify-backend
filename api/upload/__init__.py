from flask import Flask, jsonify, request
from database import get_db_uploader, get_mongodb
from flask_cors import CORS

def create_app():
	db_uploader = get_db_uploader()
	mongo_db = get_mongodb()
	app = Flask(__name__)
	CORS(app)

	print('app_name = {}'.format(app))


	@app.route('/', methods=['GET', 'POST'])
	def upload():
		certificate, sheet = request.files['certificate'], request.files['sheet']
		session_id = mongo_db.data.insert_one({}).inserted_id

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
			"session_id": str(session_id)
		})
		return response
		


	return app
