from database import get_mongodb, get_db_resource_deleter, get_db_folder_deleter
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS
from bson import ObjectId
import logging


def create_app():
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/": {"origins": "*"}})

    @app.route('/', methods=['POST'])
    def clean():
        session_id = request.json["session_id"]
        mongo_db = get_mongodb()
        db_resource_deleter, db_folder_deleter = get_db_resource_deleter(
        ), get_db_folder_deleter()

        # to delete stale records
        stale = mongo_db.data.find(
            {'time': {
                '$lt': datetime.today() - timedelta(days=1)
            }})
        mongo_db.data.delete_many(
            {'time': {
                '$lt': datetime.today() - timedelta(days=1)
            }})

        for i in stale:
            stale_session_id = i['_id']
            db_resource_deleter(f"data/{stale_session_id}/certificate",
                                resource_type="image")
            db_resource_deleter(f"data/{stale_session_id}/sheet",
                                resource_type="raw")
            db_folder_deleter(f"data/{stale_session_id}")

        # to delete or keep current session record
        current = mongo_db.data.find_one({'_id': ObjectId(session_id)})

        if current and current['stage'] == 'send':
            response = jsonify({"status": "emails are being sent"})
        else:
            mongo_db.data.delete_one({"_id": ObjectId(session_id)})
            db_resource_deleter(f"data/{session_id}/certificate",
                                resource_type="image")
            db_resource_deleter(f"data/{session_id}/sheet",
                                resource_type="raw")
            try: db_folder_deleter(f"data/{session_id}")
            except: pass

            response = jsonify({"status": "cleaned the session data"})

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.errorhandler(500)
    def server_error(e):
        logging.exception('An error occurred during a request. %s', e)
        return "An internal error occured", 500

    return app
