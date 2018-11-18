import json

from flask import Flask, request
import nltk
from nltk.stem.snowball import RussianStemmer
nltk.download('punkt')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Main page"


@app.route("/normalization", methods=["POST"])
def normalization():
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


@app.route("/detect_language", methods=["POST"])
def det_lang():
    return "detected language"


if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0', port=13502)app.run()
