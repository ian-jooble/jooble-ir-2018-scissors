import json

from flask import Flask, request

import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "main page of ranging"


@app.route('/ranking', methods=["POST"])
def ranging():
    None


if __name__ == "__main__":
    app.run(port=config.RANKING_PORT)
    # app.run(host='0.0.0.0', port=config.RANKING_PORT)

