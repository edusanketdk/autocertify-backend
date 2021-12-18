from flask import Flask, jsonify, request
from .process import process

app = Flask(__name__)


@app.route('/send/', methods=['GET', 'POST'])
def send():
    data = request.json
    process_response = process(data)
    return jsonify({"response": process_response})


if __name__ == '__main__':
	app.run(debug = True)
