import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "main page of SERP"


@app.route('/result_page', methods=["POST"])
def get_result_page():
    return "html"


if __name__ == "__main__":
    app.run(port=13504)
    # app.run(host='0.0.0.0', port=13504)

