import json

from flask import Flask, request

import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "main page of SERP"


@app.route('/result_page', methods=["POST"])
def get_result_page():
    document = json.loads(request.json, encoding="utf-8")
    serp = ""
    for i in range(min(len(document["results"]), 10)):
        res = '\033[1m' + document["results"][i]["title"] + "\033[0;0m" \
              + "\n" + "document id a.k.a. url: " + str(document["results"][i]["id"]) \
              + "\n" + document["results"][i]["snippet"]
        serp += res +"\n" + "."*100 + "\n"
    return serp


if __name__ == "__main__":
    app.run(port=config.RESULT_PAGE_PORT)
    # app.run(host='0.0.0.0', port=config.RESULT_PAGE_PORT)

