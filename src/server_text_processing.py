import json

from flask import Flask, request
import nltk
from nltk.stem.snowball import RussianStemmer
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize

nltk.download('punkt')
nltk.download('stopwords')
app = Flask(__name__)


def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

    @param text: Text whose language want to be detected
    @type text: str

    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """
    languages_ratios = {}
    words = wordpunct_tokenize(text.lower())

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
        languages_ratios[language] = len(common_elements)  # language "score"
    return languages_ratios


def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.

    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.

    @param text: Text whose language want to be detected
    @type text: str

    @return: Most scored language guessed
    @rtype: str
    """
    ratios = _calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language


def normalize_text(text):
    """Preprocess text data"""
    # Stemming
    rus_stemmer = RussianStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [rus_stemmer.stem(word) for word in text]
    # Excluding Stop-words
    text = [word for word in text if
            word not in stopwords.words('english') and word.isalpha()]
    text = " ".join(text)

    return text


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Main page of text preprocessor"


@app.route("/normalize_document", methods=["POST"])
def normalize_document():
    document = request.json
    field_for_norm = ["text", "title"]

    for field in field_for_norm:
        text = document[field]
        text = normalize_text(text)
        document[field + "_normalized"] = text

    return json.dumps(document, ensure_ascii=False)


@app.route("/normalize_query", methods=["POST"])
def normalize_query():
    text = request.json
    text = normalize_text(text)
    return text


@app.route("/detect_language", methods=["POST"])
def det_lang():
    text = request.json
    language = detect_language(text)
    return language


if __name__ == "__main__":
    app.run(port=13501)
    # app.run(host='0.0.0.0', port=13501)
