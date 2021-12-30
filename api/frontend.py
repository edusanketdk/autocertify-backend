from flask import Flask, jsonify

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def hello():
        return jsonify({"response": 'Welcome to AutoCertify'})
    
    return app