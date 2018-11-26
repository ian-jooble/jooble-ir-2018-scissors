import json

from flask import Flask, request
import nltk
from nltk.stem.snowball import RussianStemmer
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
import jsonpickle

import config
from document import Document

nltk.download('punkt')
nltk.download('stopwords')


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
    """Preprocess text data

    :param str text:
    :return str text:
    """
    # Stemming
    rus_stemmer = RussianStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [rus_stemmer.stem(word) for word in text]
    # Excluding Stop-words
    text = [word for word in text if word not in stopwords.words('english') and word.isalpha()]
    text = " ".join(text)

    return text


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Main page of text preprocessor"


@app.route("/normalize_document", methods=["POST"])
def normalize_document():
    """
    :param Document document:
    :return Document document:
    """
    document = jsonpickle.decode(request.json)
    assert isinstance(document, Document)

    text = document.text
    document.text_normalized = normalize_text(text)
    text = document.title
    document.title_normalized = normalize_text(text)

    return jsonpickle.encode(document)


@app.route("/normalize_query", methods=["POST"])
def normalize_query():
    """
    :param str text:
    :return str text:
    """
    text = request.json
    text = normalize_text(text)
    return text


@app.route("/detect_language", methods=["POST"])
def det_lang():
    """
    :param Document document:
    :return Document document: With updated language attribute
    """
    document = jsonpickle.decode(request.json)
    language = detect_language(document.text)
    document.language = language
    return jsonpickle.encode(document)


if __name__ == "__main__":
    app.run(host=config.TEXT_PROCESSING_HOST,
            port=config.TEXT_PROCESSING_PORT)
