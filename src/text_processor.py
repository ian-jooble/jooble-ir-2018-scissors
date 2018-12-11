from __future__ import print_function
from __future__ import division
from future import standard_library
import json
import sys
import os

from flask import Flask, request
from bs4 import BeautifulSoup
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from pymystem3 import Mystem
import jsonpickle
import wget
from ufal.udpipe import Model, Pipeline

from config_src import config
from document import Document

nltk.download('punkt')
nltk.download('stopwords')
standard_library.install_aliases()

udpipe_model_url = 'http://rusvectores.org/static/models/udpipe_syntagrus.model'  # URL of the UDPipe model
udpipe_filename = udpipe_model_url.split('/')[-1]

if not os.path.isfile(udpipe_filename):
    print('UDPipe model not found. Downloading...', file=sys.stderr)
    wget.download(udpipe_model_url)

print('Loading the model...', file=sys.stderr)
model = Model.load(udpipe_filename)
process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

print('Processing input...', file=sys.stderr)
for line in sys.stdin:
    res = line.strip()
    output = tag_ud(process_pipeline, text=res)
    print(' '.join(output))
    
    
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
    #languages = stopwords.fileids()
    languages = ["russian", "english"]
    
    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in languages:
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
    default_lang = "russian"
    ratios = _calculate_languages_ratios(text)
    
    # check if all ratios zero (because to short text)
    all_ratios_zero = True
    for lang in ratios.keys():
        ratio = ratios[lang]
        if ratio > 0:
            all_ratios_zero = False
            break           
    if all_ratios_zero:
        most_rated_language = default_lang
    else:
        most_rated_language = max(ratios, key=ratios.get)   

    return most_rated_language

def stemming(text, lang):
    """
    Stem the text taking into accoung language
    
    :param list of str text: list of tokens
    :return list of str text:    
    """
    stemmer = SnowballStemmer(lang)
    
    text = [stemmer.stem(word) for word in text] 
    return text


def lemmatization(text, lang, pos, pipeline):
    """
    Lemmatize the text taking into accoung language
    
    :param list of str text: list of tokens
    :param bool pos: if True add tags to tokens like "_NOUN"
    :param Pipeline pipeline:
    :return list of str text:    
    """  
    if lang == "russian":
        #lemmatizer = Mystem()
        text = " ".join(text)
        text = tag_ud(pipeline, text=text, pos=pos)
        #text = lemmatizer.lemmatize(text)             
    else:
        lemmatizer = WordNetLemmatizer()
        text = [lemmatizer.lemmatize(word) for word in text] 
    return text
  
    
def clean_html(text):
    """
    Clean text from html tags
    
    :param str text:
    :return str text:
    """
    try:
        text = BeautifulSoup(text, "html").text
    except:
        print("Exception in  clean_html. NoneType argument.")
        return ""
    
    return text


def normalize_text(text, norm_type="stemming", pos=False, pipeline=None):
    """
    Preprocess text data
    
    :param str text:
    :param str norm_type: "stemming" or "lemmatization" of None
    :param bool pos: Only for lemmatization. If True add tags to tokens like "_NOUN"
    :param Pipeline pipeline: for lemmatization
    :return str text:
    """
    text = clean_html(text)
    text = text.lower()
    lang = detect_language(text)
    text = nltk.word_tokenize(text)
    
    # Excluding Stop-words
    text = [word for word in text if
            word not in stopwords.words(lang) and word.isalpha()]
    
    if lang not in SnowballStemmer.languages:
        lang = "english"
     
    if isinstance(norm_type, type(None)):
        pass
    elif norm_type.lower() == "lemmatization":
        text = lemmatization(text, lang, pos, pipeline)
    elif norm_type.lower() == "stemming":
        text = stemming(text, lang)

    text = " ".join(text)   
    return text


def tag_ud(pipeline, text='Текст нужно передать функции в виде строки!', pos=False):
    # если частеречные тэги не нужны (например, их нет в модели), выставьте pos=False
    # в этом случае на выход будут поданы только леммы

    # обрабатываем текст, получаем результат в формате conllu:
    processed = pipeline.process(text)

    # пропускаем строки со служебной информацией:
    content = [l for l in processed.split('\n') if not l.startswith('#')]

    # извлекаем из обработанного текста лемму и тэг
    tagged = [w.split('\t')[2].lower() + '_' + w.split('\t')[3] for w in content if w]

    tagged_propn = []
    propn = []
    for t in tagged:
        if t.endswith('PROPN'):
            if propn:
                propn.append(t)
            else:
                propn = [t]
        elif t.endswith('PUNCT'):
            propn = []
            continue  # я здесь пропускаю знаки препинания, но вы можете поступить по-другому
        else:
            if len(propn) > 1:
                name = '::'.join([x.split('_')[0] for x in propn]) + '_PROPN'
                tagged_propn.append(name)
            elif len(propn) == 1:
                tagged_propn.append(propn[0])
            tagged_propn.append(t)
            propn = []
    if not pos:
        tagged_propn = [t.split('_')[0] for t in tagged_propn]
    return tagged_propn


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


@app.route("/stem_text", methods=["POST"])
def stem_text():
    """
    :param str text:
    :return str text: 
    """
    text = request.json
    text = normalize_text(text, norm_type="stemming")
    return text


@app.route("/lemmatize_text", methods=["POST"])
def lemmatize_text():
    """
    :param str text:
    :return str text: 
    """
    text = request.json
    text = normalize_text(text, norm_type="lemmatization",
                          pos=False, pipeline=process_pipeline)
    return text


@app.route("/tag_text", methods=["POST"])
def tag_text():
    """
    :param str text:
    :return str text: 
    """
    text = request.json
    text = normalize_text(text, norm_type="lemmatization",
                          pos=True, pipeline=process_pipeline)
    return text


@app.route("/tokenize_text", methods=["POST"])
def tokenize_text():
    """
    :param str text:
    :return str text: 
    """
    text = request.json
    text = normalize_text(text, norm_type=None)
    return text


@app.route("/detect_language", methods=["POST"])
def det_lang():
    """
    :param str text:
    :return str language:
    """
    text = request.json
    language = detect_language(text)
    return language


if __name__ == "__main__":
    app.run(host=config.TEXT_PROCESSING_HOST,
            port=config.TEXT_PROCESSING_PORT)
