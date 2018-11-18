import json

import requests
from flask import Flask, request

# global variables for storing information
inverted_index = {}
forward_index = []
documents_id = []

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "main page of indexator"


@app.route('/indexator', methods=["POST"])
def add_to_index():
    return "added to index"


@app.route("/search", methods=["POST"])
def search():
    return json.dumps(result)


if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0', port=13502)app.run()
