import requests
from flask import Flask, request, render_template
from wtforms import Form, TextField, validators

import config

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
    Parameters:
    query: str

    Returns
    dictionary like {"lang": "language", "text": query, "stemmed_text": stemme
    """
    form = ReusableForm(request.form)
    if request.method == 'POST':
        query = request.form['name']
        print(text_processing_url + "normalize_query")
        r = requests.post(text_processing_url + "normalize_query", json=query)
        search_query = r.text
        r = requests.post(indexer_url + "search", json=search_query)
        search_results = r.text
        r = requests.post(snippets_url + "snippets", json=search_results)
        snipets = r.text
        r = requests.post(res_page_form_url + "result_page", json=snipets)
        result_page = r.text
        return result_page
    else:
        return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(port=config.MANAGER_PORT)
    # app.run(host='0.0.0.0', port=config.MANAGER_PORT)
