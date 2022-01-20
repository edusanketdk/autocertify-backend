from flask import Flask, jsonify, request
from create_report import create_report
from mark_stage import mark_stage
from flask_cors import CORS
from process import process
import logging



def create_app():
	app = Flask(__name__)
	app.config['CORS_HEADERS'] = 'Content-Type'
	CORS(app, resources={r"/": {"origins": "*"}})
	

	@app.route('/', methods=['POST'])
	def send():
		data = request.json

		mark_stage(data['session_id'], 'send')
		process(data)
		mark_stage(data['session_id'], 'completed')

		create_report(data['user_email'])

		response = jsonify({"response": "sent"})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response


	@app.errorhandler(500)
	def server_error(e):
		logging.exception('An error occurred during a request. %s', e)
		return "An internal error occured", 500


	return app
