"""This service contains forward_index, inverted_index and list of documents_id.

Structure of forward_index:
    dict {"id_doc1": Document instance1,
          "id_doc2": Document instance2,
          ...}

Structure of inverted_index:
    dict {"term1": [{"id": "doc1_id", "pos": [list of int], "pos_raw": [list of int]},
                    {"id": "doc5_id", "pos": [list of int], "pos_raw": [list of int]}
                    ...],
          "term2": [{"id": "doc3_id", "pos": [list of int], "pos_raw": [list of int]},
                    {"id": "doc5_id", "pos": [list of int], "pos_raw": [list of int]},
                    ...],
          ...}

Structure of documents_id:
    list of str ["id_doc1", "213343", ...]


It contains functions:
    - save_index
    - load_index
    - search_boolean
    - add_forward_index
    - add_inverted_index
"""

import json
import re
import os

from flask import Flask, request
import nltk
import jsonpickle

import config

nltk.download('punkt')

forward_index = {}
inverted_index = {}
documents_id = []


def save_index(path, forward_index, inverted_index, documents_id,
               forward_file="forward_index",
               inverted_file="inverted_index",
               id_file="documents_id"):
    """Save index as json files

    :param str path: path to folder
    :param dict forward_index: link to forward_index instance.
    :param dict inverted_index: link to inverted_index instance.
    :param list of str documents_id: link to documents_id  instance.

    :param str forward_file: file name for forward_index without extension.
    :param str inverted_file: file name for inverted_index without extension.
    :param str id_file: file name for documents_id without extension.
    """

    file_path = os.path.join(path, forward_file + ".json")
    with open(file_path, 'w', encoding='utf8') as outfile:
        forward_index = jsonpickle.encode(forward_index)
        json.dump(forward_index, outfile, ensure_ascii=False)

    file_path = os.path.join(path, inverted_file + ".json")
    with open(file_path, 'w', encoding='utf8') as outfile:
        inverted_index = jsonpickle.encode(inverted_index)
        json.dump(inverted_index, outfile, ensure_ascii=False)

    file_path = os.path.join(path, id_file + ".json")
    with open(file_path, 'w') as outfile:
        documents_id = jsonpickle.encode(documents_id)
        json.dump(documents_id, outfile)


def load_index(path, forward_file="forward_index",
               inverted_file="inverted_index",
               id_file="documents_id"):
    """Load index from files.

    If files don't exist, return empty entities.

    :return dict forward_index:
    :return dict inverted_index:
    :return list of int documents_id:
    """
    forward_index = {}
    inverted_index = {}
    documents_id = []

    file_path_forw = os.path.join(path, forward_file + ".json")
    file_path_inv = os.path.join(path, inverted_file + ".json")
    file_path_id = os.path.join(path, id_file + ".json")

    files_present = os.path.exists(file_path_forw) and \
                    os.path.exists(file_path_inv) and \
                    os.path.exists(file_path_id)

    if files_present:
        with open(file_path_forw, 'r', encoding='utf8') as infile:
            forward_index = json.load(infile)
            forward_index = jsonpickle.decode(forward_index)

        with open(file_path_inv, 'r', encoding='utf8') as infile:
            inverted_index = json.load(infile)
            inverted_index = jsonpickle.decode(inverted_index)

        with open(file_path_id, 'r', encoding='utf8') as infile:
            documents_id = json.load(infile)
            documents_id = jsonpickle.decode(documents_id)

    return forward_index, inverted_index, documents_id


def search_boolean(search_query, forward_index, inverted_index, documents_id):
    """Search the words of search_query in inverted index

    :param str search_query:
    :param dict forward_index:
    :param dict inverted_index:
    :param list of str documents_id:

    :return dict like {"documents": documents, "terms": terms} where:
            documents - list of Document instances,
            terms - list of dicts like {"term": "word1",
                                        "inverted_index": [dict1, dict2, ...]
    :rtype: dict

    :return "Documents aren't found.": If no document is found.
    :rtype: str
    """

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
            terms.append(
                {"term": word,
                 "inverted_index": [doc for doc in inverted_index[word]
                                    if doc['id'] in set_of_docs_id]})
        return {"documents": documents, "terms": terms}
    else:
        return "Documents aren't found."


def add_forward_index(document, forward_index):
    """Add the document to forward index.

    :param Document document:
    :param dict forward_index:

    :return dict forward_index: Updated with new document.
    """
    forward_index[str(document.id)] = document
    return forward_index


def add_inverted_index(document, inverted_index):
    """Add the document to inverted index.

    :param Document document:
    :param dict inverted_index:

    :return dict inverted_index: Updated with new document.
    """
    tokens = nltk.word_tokenize(document.text_normalized)
    for token in tokens:
        positions_raw = [s.start() for s
                         in re.finditer(token, document.text)]
        positions = [s.start() for s
                     in re.finditer(token, document.text_normalized)]
        token_inv_idx = {"id": str(document.id),
                         "pos": positions,
                         "pos_raw": positions_raw}
        if token in inverted_index.keys():
            inverted_index[token].append(token_inv_idx)
        else:
            inverted_index[token] = [token_inv_idx]
    return inverted_index


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Main page of indexer"


@app.route('/indexer', methods=["POST"])
def add_to_index():
    """
    :param Document document:
    :return str: Status of adding.
    """
    global forward_index
    global inverted_index
    global documents_id

    document = jsonpickle.decode(request.json)
    if str(document.id) not in documents_id:
        documents_id.append(str(document.id))
        forward_index = add_forward_index(document, forward_index)
        inverted_index = add_inverted_index(document, inverted_index)
        return "document is successfully added."
    else:
        return "document already exist in index."


@app.route("/search", methods=["POST"])
def search():
    """
    :param str search_query:
    :return dict: Dictionary like {"documents": documents, "terms": terms}, where
                  documents - list of Document instances,
                  terms - list of dicts,{"term": "word1",
                                        "inverted_index": [dict1, dict2, ...]}

    :return "Documents aren't found.": If no document is found.
    :rtype: str
    """
    search_query = request.json
    search_result = search_boolean(search_query, forward_index,
                                   inverted_index, documents_id)
    return jsonpickle.encode(search_result)


@app.route("/save_index", methods=["POST"])
def saving():
    """Save current state of index."""

    save_index(config.data_dir, forward_index, inverted_index, documents_id)
    return "successfully saved."


if __name__ == "__main__":
    forward_index, inverted_index, documents_id = load_index(config.data_dir)

    app.run(host=config.INDEXER_HOST, port=config.INDEXER_PORT)
