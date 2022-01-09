from flask import Flask, jsonify, request, logging
from process import process
from flask_cors import CORS, cross_origin


def create_app():
	app = Flask(__name__)
	app.config['CORS_HEADERS'] = 'Content-Type'
	CORS(app, resources={r"/foo": {"origins": "*"}})
	

	@app.route('/', methods=['POST'])
	def send():
		data = request.json
		process(data)
		response = jsonify({"response": "sent"})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

	@app.errorhandler(500)
	def server_error(e):
		logging.exception('An error occurred during a request. %s', e)
		return "An internal error occured", 500

	return app
