from flask import Flask, jsonify, request
from database import get_mongodb, get_db_deleter
from bson import ObjectId


def create_app():
	app = Flask(__name__)
	print('app_name = {}'.format(app))

	@app.route('/', methods=['GET', 'POST'])
	def clean():
		session_id = request.json["session_id"]
		mongo_db = get_mongodb()

		mongo_db.data.delete_one({"_id": ObjectId(session_id)})

		db_deleter = get_db_deleter()
		db_deleter(f"data/{session_id}")
		
		return jsonify({"status": "cleaned the session data"})

	return app

