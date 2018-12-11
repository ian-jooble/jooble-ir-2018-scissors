import json

from flask import Flask, request
import jsonpickle

import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "main page of SERP"


@app.route('/result_page', methods=["POST"])
def get_result_page():
    """
    :param dict params: Like {"documents": [list of Documents],
                              "query": str query}

    :return str serp: Search engine result page
    """
    params = jsonpickle.decode(request.json)
    documents = params["documents"]
    query = params["query"]
    serp = ""
    for i in range(min(len(documents), 10)):
        res = '\033[1m' + documents[i].title + "\033[0;0m" + "\n" + "document id a.k.a. url: " + str(
            documents[i].id) + "\n" + documents[i].snippet
        serp += res + "\n" + "." * 100 + "\n"
    return serp


if __name__ == "__main__":
    app.run(host=config.RESULT_PAGE_HOST,
            port=config.RESULT_PAGE_PORT)

