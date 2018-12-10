import json

import requests
from flask import Flask, request, render_template
from wtforms import Form, TextField, validators
import jsonpickle

import config
from document import Document

indexer_url = config.indexer_url
text_processing_url = config.text_processing_url
ranking_url = config.ranking_url
snippets_url = config.snippets_url
res_page_form_url = config.res_page_form_url


class ReusableForm(Form):
    name = TextField('Enter your request:', validators=[validators.DataRequired()])


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    If GET -> renders Main page from templates/index.html
    If POST -> renders ranged search results
    """
    form = ReusableForm(request.form)
    if request.method == 'POST':
        query = request.form['name']

        # Normilize search query
        r = requests.post(text_processing_url + config.NORMALIZE_QUERY_PATH,
                          json=query)
        search_query = r.text

        # Search
        r = requests.post(indexer_url + config.SEARCH_PATH,
                          json=search_query)
        search_result = jsonpickle.decode(r.text)
        documents = search_result["documents"]
        terms = search_result["terms"]

        # Ranking
        search_result = {"documents": documents,
                         "query": search_query}
        r = requests.post(ranking_url + config.RANK_PATH,
                          json=jsonpickle.encode(search_result))
        search_result = jsonpickle.decode(r.text)

        # Get snippets
        search_result = {"documents": [i[1] for i in search_result],
                         "terms": terms}
        r = requests.post(snippets_url + config.SNIPPETS_PATH,
                          json=jsonpickle.encode(search_result))
        search_result = jsonpickle.decode(r.text)

        # SERP
        search_result = {"documents": search_result,
                         "query": search_query}
        r = requests.post(res_page_form_url + config.RESULT_PAGE_PATH,
                          json=jsonpickle.encode(search_result))
        result_page = r.text
        return result_page
    else:
        return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(host=config.MANAGER_HOST, port=config.MANAGER_PORT)
