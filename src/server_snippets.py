import json

from flask import Flask, request

import config

app = Flask(__name__)


@app.route('/snippets', methods=["POST"])
def get_snippets():
    document = json.loads(request.json, encoding="utf-8")
    
    documents = document["documents"]
    terms = []
    for term in document["terms"]:
        terms.append(term["inverted_index"][0]["pos"][0])
    
    result_lists = []
    for doc in documents:
        if terms[0] < 10 and terms[1] < 200:
            snippet = doc["text"][0:min(180, len(doc["text"]) - 1)]
        
        elif terms[0] > 10 :
            snippet = doc["text"][terms[0]:min(terms[0]+180, len(doc["text"]) - 1)]

        elif terms[0] > 10 and  terms[1] > 210:
            snippet = doc["text"][terms[0]:min(terms[0] + 90, len(doc["text"]) - 1)]
            snippet = snippet + " ... " + doc["text"][terms[1]:min(terms[1] + 90, len(doc["text"]) - 1)]
            
        doc["snippet"] = snippet    
    search_res = dict()
    search_res["results"] = documents
    return json.dumps(search_res, ensure_ascii=False)


if __name__ == "__main__":
    app.run(port=config.SNIPPETS_PORT)
    # app.run(host='0.0.0.0', port=config.SNIPPETS_PORT)
