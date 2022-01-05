from flask import Flask, jsonify

def create_app():
	app = Flask(__name__, instance_relative_config=True)

	@app.route("/")
	def hello():
		response = jsonify({"response": 'Welcome to AutoCertify'})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

	return app