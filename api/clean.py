from flask import Flask, jsonify, request
from database import get_mongodb, get_db_deleter


def create_app():
	app = Flask(__name__)

	@app.route('/clean/', methods=['GET', 'POST'])
	def clean():
		session_id = request.json["session_id"]
		mongo_db = get_mongodb()

		mongo_db.data.delete_one({"_id": session_id})

		db_deleter = get_db_deleter()
		db_deleter(f"data/{session_id}/certificate")
		db_deleter(f"data/{session_id}/sheet")
		
		return jsonify({})

	return app

