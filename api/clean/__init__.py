from flask import Flask, jsonify, request
from database import get_mongodb, get_db_resource_deleter, get_db_folder_deleter
from bson import ObjectId
from flask_cors import CORS



def create_app():
	app = Flask(__name__)
	CORS(app)
	print('app_name = {}'.format(app))

	@app.route('/', methods=['GET', 'POST'])
	def clean():
		
		session_id = request.json["session_id"]
		mongo_db = get_mongodb()

		mongo_db.data.delete_one({"_id": ObjectId(session_id)})

		db_resource_deleter, db_folder_deleter = get_db_resource_deleter(), get_db_folder_deleter()
		db_resource_deleter(f"data/{session_id}/certificate", resource_type="image")
		db_resource_deleter(f"data/{session_id}/sheet", resource_type="raw")
		db_folder_deleter(f"data/{session_id}")
		
		response =  jsonify({"status": "cleaned the session data"})
		return response

	return app

