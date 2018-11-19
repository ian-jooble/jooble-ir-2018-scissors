import json

from flask import Flask, request
import nltk
from nltk.stem.snowball import RussianStemmer

nltk.download('punkt')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Main page of text preprocessor"


@app.route("/normalize_document", methods=["POST"])
def normalize_document():
    document = request.json
    field_for_norm = ["text", "title"]
    rus_stemmer = RussianStemmer()

    for field in field_for_norm:
        text = document[field].lower()
        text = nltk.word_tokenize(text)
        text = [rus_stemmer.stem(word) for word in text]
        text = " ".join(text)
        document[field + "_normalized"] = text

    return json.dumps(document, ensure_ascii=False)


@app.route("/normalize_query", methods=["POST"])
def normalize_string():
    query = request.json
    rus_stemmer = RussianStemmer()
    text = query.lower()
    text = nltk.word_tokenize(text)
    text = [rus_stemmer.stem(word) for word in text]
    text = " ".join(text)
    return text


@app.route("/detect_language", methods=["POST"])
def det_lang():
    return "detected language"


if __name__ == "__main__":
    app.run(port=13501)
    # app.run(host='0.0.0.0', port=13501)
