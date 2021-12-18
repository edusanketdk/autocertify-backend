from flask import Flask, jsonify, request
from .process import process
from .database import get_mongodb, db_deleter

app = Flask(__name__)


@app.route('/clean/', methods=['GET', 'POST'])
def clean():
    session_id = request.json["session_id"]
    mongo_db = get_mongodb()

    mongo_db.data.delete_one({"_id": session_id})
    db_deleter(f"data/{session_id}/certificate")
    db_deleter(f"data/{session_id}/sheet")
    
    return jsonify({})


if __name__ == '__main__':
	app.run(debug = True)
