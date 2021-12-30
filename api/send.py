from flask import Flask, jsonify, request
from api.process import process


def create_app():
	app = Flask(__name__)

	@app.route('/send/', methods=['GET', 'POST'])
	def send():
		data = request.json
		process_response = process(data)
		return jsonify({"response": process_response})

	return app
