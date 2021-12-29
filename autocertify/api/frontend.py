from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def hello():
        return {'Welcome to AutoCertify'}
    
    return app