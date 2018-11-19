import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/snippets', methods=["POST"])
def get_snippets():
    None


if __name__ == "__main__":
    app.run(port=13503)
    # app.run(host='0.0.0.0', port=13503)
