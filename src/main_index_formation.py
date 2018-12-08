import json
import gzip
import os
import time

import requests
import pandas as pd

import jsonpickle

import config
from document import Document

indexer_url = config.indexer_url
text_processing_url = config.text_processing_url
ranking_url = config.ranking_url
snippets_url = config.snippets_url
res_page_form_url = config.res_page_form_url


def load_data(data_path):
    """
    Load all data to pandas.DataFrame

    :param str data_path: Path to folder with data
    :return pd.DataFrame data:
    """
    docs_info = []
    docs_text = []
    file_names = os.listdir(data_path)

    for file in file_names:
        if "text" in file:
            with gzip.open(os.path.join(data_path, file), "rb") as f:
                for line in f:
                    vacancy = json.loads(line)
                    docs_text.append(vacancy)
        else:
            with gzip.open(os.path.join(data_path, file), "rb") as inf:
                for line in inf:
                    vacancy = json.loads(line)
                    docs_info.append(vacancy)

    assert len(docs_info) == len(docs_text)
    assert "id" in docs_info[0].keys()
    assert "id_job" in docs_text[0].keys()

    docs_info = pd.DataFrame(docs_info)
    docs_text = pd.DataFrame(docs_text)
    docs_info.drop_duplicates(["id"], inplace=True)
    docs_text.drop_duplicates(["id_job"], inplace=True)
    data = docs_info.merge(docs_text, left_on='id', right_on='id_job', how='outer')

    return data


def add_documents_to_index(documents):
    """
    Add the document from pd.DataFrame to index.

    :param pandas.DataFrame documents:
    """
    for index, row in documents.iterrows():
        doc_id = row["id"]
        title = row["title"]
        text = row["text"]
        language = row["lang_text"]
        doc = Document(doc_id, title, text, language)
        r = requests.post(text_processing_url + config.NORMALIZE_DOC_PATH,
                          json=jsonpickle.encode(doc))
        status_normalizer = r.status_code
        doc_normalized = jsonpickle.decode(r.text)

        r = requests.post(indexer_url + config.INDEXER_PATH,
                          json=jsonpickle.encode(doc_normalized))
        status_indexer = r.status_code

        if status_indexer != 200 or status_normalizer != 200:
            print(" Request number", index, ": ")
            print("error")
    print("dataset adding finished!")


dataset = load_data(config.dataset_dir)

# Run this cell only once
# Adding may takes from 15min (for 30k docs) to 1 hour
# Index with 30k documents takes about 2-3 Gb RAM
# 5k documents enough for testing during development

n_docs = 5000
start = time.time()
add_documents_to_index(dataset.loc[:n_docs])
print("Adding time =", time.time() - start)

# Save current status of index

r = requests.post(indexer_url + "save_index")
print(r.status_code)

print("Normalize the document.")
row = dataset.loc[1001, :]
doc_id = row["id"]
title = row["title"]
text = row["text"]
language = row["lang_text"]
doc = Document(doc_id, title, text, language)

r = requests.post(text_processing_url + config.NORMALIZE_DOC_PATH,
                  json=jsonpickle.encode(doc))
status_normalizer = r.status_code
doc_normalized = jsonpickle.decode(r.text)
print(doc_normalized)

print("\nAdding the document to index")
r = requests.post(indexer_url + config.INDEXER_PATH,
                  json=jsonpickle.encode(doc_normalized))
print(r.status_code)
print(r.text)

print("\nNormilize query \"водитель\".")
query = "водитель"
r = requests.post(text_processing_url + config.NORMALIZE_QUERY_PATH,
                  json=query)
print(r.status_code)
search_query = r.text
print(search_query)

print("\nSearch in index.")
r = requests.post(indexer_url + config.SEARCH_PATH, json=search_query)
print(r.status_code)
search_result = jsonpickle.decode(r.text)
print(search_result["documents"][:2])

documents = search_result["documents"]
terms = search_result["terms"]

print("\nRanking the document")
docs_query = {"documents": documents, "query": search_query}
r = requests.post(ranking_url + config.RANK_PATH,
                  json=jsonpickle.encode(docs_query))
print(r.status_code)
rank_result = jsonpickle.decode(r.text)
print("len = ", len(rank_result))
print(rank_result[:2])

print("\nGet snippets.")
docs_query = {"documents": [i[1] for i in rank_result], "terms": terms}
r = requests.post(snippets_url + config.SNIPPETS_PATH,
                  json=jsonpickle.encode(docs_query))
print(r.status_code)
rank_result = jsonpickle.decode(r.text)
print(rank_result[:2])

print("\nSERP results")
docs_query = {"documents": rank_result, "query": search_query}
r = requests.post(res_page_form_url + config.RESULT_PAGE_PATH,
                  json=jsonpickle.encode(docs_query))
print(r.status_code)
search_result = r.text
print(search_result)


