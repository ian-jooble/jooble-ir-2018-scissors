import json

import requests
from flask import Flask, request


app = Flask(__name__)


@app.route('/snippets', methods=["POST"])
def get_snippets(q=None):
    None


if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0', port=13502)app.run()
