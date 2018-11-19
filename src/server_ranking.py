import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "main page of ranging"


@app.route('/ranging', methods=["POST"])
def ranging():
    None


if __name__ == "__main__":
    app.run(port=13502)
    # app.run(host='0.0.0.0', port=13502)

