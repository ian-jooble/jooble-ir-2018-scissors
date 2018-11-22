import json
import gzip
import os
import time

import requests
import pandas as pd

import config

indexer_url = config.indexer_url
text_processing_url = config.text_processing_url
ranking_url = config.ranking_url
snippets_url = config.snippets_url
res_page_form_url = config.res_page_form_url


def test_system():
    r = requests.post(indexer_url)
    print(r.status_code)
    print(r.text)

    #  normalize the document
    r = requests.post(text_processing_url + "normalize_document",
                      json={"id": 7, "title": "Садоводство",
                            "text": "Саженцы декоративных и плодовых культур. "
                                    "Могилев. Гарантия."})
    print(r.status_code)
    print(json.loads(r.text))
    document = json.loads(r.text, encoding="utf-8")

    #  add the document to index
    r = requests.post(indexer_url + "indexer", json=document)
    print(r.status_code)
    print(r.text)

    #  normalize the search query
    r = requests.post(text_processing_url + "normalize_query",
                      json="плодовые культуры")
    print(r.status_code)
    print(str(r.text))
    search_query = r.text

    # search in index
    r = requests.post(indexer_url + "search", json=search_query)
    print(r.status_code)
    print(r.text)

    # search in index
    r = requests.post(indexer_url + "search", json="водител")
    print(r.status_code)
    print(r.text)
    print(json.loads(r.text, encoding="utf-8"))


def load_data(data_path):
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


def add_dataset_to_index(dataset):
    for index, row in dataset.iterrows():
        r = requests.post(text_processing_url + "normalize_document", json=row.to_dict())
        status_normilizer = r.status_code
        doc_normilized = json.loads(r.text)
        r = requests.post(indexer_url + "indexer", json=doc_normilized)
        status_indexer = r.status_code

        if status_indexer != 200 or status_normilizer != 200:
            print(" Request number", index, ": ")
            print("error")
    print("dataset adding finished!")


dataset_path = os.path.join("..", "data", "by_jobs", "by")
documents = load_data(dataset_path)
print("Number of documents =", len(documents))
print("Text of first five documents:")
print(documents.head()["text"])

start = time.time()
add_dataset_to_index(documents.loc[:30000])
print("Adding time =", time.time() - start)
r = requests.post(indexer_url + "save_index")
#  search in index
# r = requests.post(indexer_url + "search", json="вектор")
# print(r.status_code)
# print(r.text)
# print(json.loads(r.text, encoding="utf-8"))

# -------##--------##--------##--------##--------##--------##--------##--------#

