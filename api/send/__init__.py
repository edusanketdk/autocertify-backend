from flask import Flask, jsonify, request
from process import process
from flask_cors import CORS


def create_app():
	app = Flask(__name__)
	CORS(app)
	print('app_name = {}'.format(app))

	@app.route('/', methods=['GET', 'POST'])
	def send():
		data = request.json
		process(data)
		response = jsonify({"response": "sent"})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

	return app
