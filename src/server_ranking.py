import json
import pickle
import os

from flask import Flask, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jsonpickle

import config

vectorizer = None
tfidf = None


def load_index(path, forward_file="forward_index", inverted_file="inverted_index", id_file="documents_id"):
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

    files_present = os.path.exists(file_path_forw) and os.path.exists(file_path_inv) and os.path.exists(file_path_id)

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


def compute_tfidf(forward_index, documents_id):
    corpus = []
    for i in documents_id:
        corpus.append(forward_index[i].text_normalized)

    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.5, ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(corpus).todense()
    return vectorizer, tfidf


def initialize_tfidf(index_path, save_tfidf_path):
    forward_index, _, documents_id = load_index(index_path)
    vectorizer, tfidf = compute_tfidf(forward_index, documents_id)

    save_tfidf_path = os.path.join(save_tfidf_path, "vectorizer_tfidf.dat")
    with open(save_tfidf_path, "wb") as ouf:
        pickle.dump(vectorizer, ouf)
        pickle.dump(tfidf, ouf)

    return vectorizer, tfidf


def ranking(documents, query, vectorizer, tfidf):
    query_vect = vectorizer.transform([query]).todense()
    doc_vects = [doc.text_normalized for doc in documents]
    doc_vects = vectorizer.transform(doc_vects).todense()

    ranked_list = cosine_similarity(doc_vects, query_vect)
    ranked_list = list(np.squeeze(ranked_list, axis=1))
    assert (len(ranked_list) == len(documents))

    ranked_list = list(zip(ranked_list, documents))
    ranked_list = sorted(ranked_list, key=lambda x: x[0])
    ranked_list = list(reversed(ranked_list))

    return ranked_list


app = Flask(__name__)


@app.route('/ranking', methods=["POST"])
def get_ranked():
    """
    Return list of ranked documents.

    Get params from request.json

    :param dict params: {"documents": [list of Document],
                         "query": str search_query}

    :return list of tuples  ranked_list: Where (float rank,
                                                Document document)
    """
    params = jsonpickle.decode(request.json)
    if isinstance(params, dict):
        documents = params["documents"]
        query = params["query"]
        ranked_list = ranking(documents, query, vectorizer, tfidf)
        return jsonpickle.encode(ranked_list)
    else:
        return jsonpickle.encode("Documents aren't found")


if __name__ == "__main__":
    vectorizer, tfidf = initialize_tfidf(config.data_dir,
                                         config.data_dir)
    app.run(host=config.RANKING_HOST, port=config.RANKING_PORT)

