import json
import re

from flask import Flask, request
import jsonpickle

import config


app = Flask(__name__)


@app.route('/snippets', methods=["POST"])
def get_snippets():
    """
    :param dict params: Like {"documents": [list of Documents],
                              "terms":  list of dicts [{"term": "word1",
                                        "inverted_index": [dict1, dict2, ...]}]}

    :return list of Documents documents: With updated snippet attributes
    """
    params = jsonpickle.decode(request.json)
    documents = params["documents"]
    search_terms = params["terms"]
    query = " ".join([i["term"] for i in search_terms])

    for doc in documents:
        doc.snippet = doc.text[:100]

    return jsonpickle.encode(documents)


if __name__ == "__main__":
    app.run(host=config.SNIPPETS_HOST, port=config.SNIPPETS_PORT)

