import json
import re
import os

from flask import Flask, request
import nltk

import config

nltk.download('punkt')
inverted_index = {}
forward_index = {}
documents_id = []


def save_index(path):
    file_path = os.path.join(path, "forward_index.json")
    with open(file_path, 'w', encoding='utf8') as outfile:
        json.dump(forward_index, outfile, ensure_ascii=False)

    file_path = os.path.join(path, "inverted_index.json")
    with open(file_path, 'w', encoding='utf8') as outfile:
        json.dump(inverted_index, outfile, ensure_ascii=False)

    file_path = os.path.join(path, "documents_id.json")
    with open(file_path, 'w') as outfile:
        json.dump(documents_id, outfile)


def load_index(path):
    global forward_index
    global inverted_index
    global documents_id

    file_path = os.path.join(path, "forward_index.json")
    with open(file_path, 'r', encoding='utf8') as infile:
        forward_index = json.load(infile)

    file_path = os.path.join(path, "inverted_index.json")
    with open(file_path, 'r', encoding='utf8') as infile:
        inverted_index = json.load(infile)

    file_path = os.path.join(path, "documents_id.json")
    with open(file_path, 'r', encoding='utf8') as infile:
        documents_id = json.load(infile)


def search_boolean(search_query):
    """Search the words of search_query in inverted index"""
    docs_id = []
    words = search_query.split(" ")

    for word in words:
        if word in inverted_index.keys():
            docs_id.append(set([doc["id"] for doc in inverted_index[word]]))

    if len(docs_id) > 0:
        set_of_docs_id = docs_id[0]
        for docs_set in docs_id:
            set_of_docs_id = set_of_docs_id.intersection(docs_set)

        documents = []
        terms = []
        set_of_docs_id = list(set_of_docs_id)
        for id in set_of_docs_id:
            documents.append(forward_index[str(id)])
        for i, word in enumerate(words):
            terms.append({"term": word,
                          "inverted_index": [doc for doc in inverted_index[word]
                                             if doc['id'] in set_of_docs_id]})
        return {"documents": documents, "terms": terms}
    else:
        return "Documents aren't found."


def add_forward_index(document):
    """Add the document to forward index"""
    global forward_index
    forward_index[str(document["id"])] = document


def add_inverted_index(document):
    """Add the document to inverted index"""
    tokens = nltk.word_tokenize(document["text_normalized"])
    for token in tokens:
        count = tokens.count(token)
        token_len = len(token)
        count_title = document["title_normalized"].count(token)
        positions_raw = [s.start() for s in re.finditer(token,
                                                        document["text"])]
        positions = [s.start() for s in re.finditer(token,
                                                    document["text_normalized"])]
        token_inv_idx = {"id": int(document["id"]),
                         "count": count,
                         "count_title": count_title,
                         "length": token_len,
                         "pos": positions,
                         "pos_raw": positions_raw}
        if token in inverted_index.keys():
            inverted_index[token].append(token_inv_idx)
        else:
            inverted_index[token] = [token_inv_idx]


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Main page of indexer"


@app.route('/indexer', methods=["POST"])
def add_to_index():
    document = request.json
    if document["id"] not in documents_id:
        documents_id.append(document["id"])
        add_forward_index(document)
        add_inverted_index(document)
        return "document is successfully added."
    else:
        return "document already exist in index."


@app.route("/search", methods=["POST"])
def search():
    search_query = request.json
    return json.dumps(search_boolean(search_query), ensure_ascii=False)


@app.route("/save_index", methods=["POST"])
def saving():
    save_index(config.data_dir)
    return "successfully saved."


if __name__ == "__main__":
    load_index(config.data_dir)
    app.run(port=config.INDEXER_PORT)
    # app.run(host='0.0.0.0', port=config.INDEXER_PORT)
