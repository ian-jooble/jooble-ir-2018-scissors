import os

base_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(base_dir, 'src')
data_dir = os.path.join(base_dir, 'data')
jooble_data_dir = os.path.join(data_dir, "by_jobs")
index_dir = os.path.join(data_dir, "index")
headhunter_dir = os.path.join(data_dir, "HeadHunter_data")

class_data_dir = os.path.join(src_dir, "model",
                              "classifier_train_data",
                              "hh_dataset_all_uniq_text.csv")
class_vect_dir = os.path.join(src_dir, "model",
                              "classifier_train_data",
                              "vectorizer_tfidf.dat")

INDEXER_PORT = 13500
TEXT_PROCESSING_PORT = 13501
RANKING_PORT = 13502
SNIPPETS_PORT = 13503
RESULT_PAGE_PORT = 13504
MANAGER_PORT = 13505

SEARCH_PATH = "search"
INDEXER_PATH = "indexer"
RANK_PATH = "ranking"

NORMALIZE_DOC_PATH = "normalize_document"
NORMALIZE_QUERY_PATH = "normalize_query"
STEM_TEXT_PATH = "stem_text"
LEMM_TEXT_PATH = "lemmatize_text"
TAG_TEXT_PATH = "tag_text"
TOKEN_TEXT_PATH = "tokenize_text"
DETECT_LANG_PATH = "detect_language"

SNIPPETS_PATH = "snippets"
RESULT_PAGE_PATH = "result_page"

# MANAGER_HOST = "0.0.0.0"
MANAGER_HOST = "127.0.0.1"
INDEXER_HOST = MANAGER_HOST
TEXT_PROCESSING_HOST = MANAGER_HOST
RANKING_HOST = MANAGER_HOST
SNIPPETS_HOST = MANAGER_HOST
RESULT_PAGE_HOST = MANAGER_HOST

#MAIN_URL = "http://0.0.0.0:"
MAIN_URL = "http://127.0.0.1:"

indexer_url = MAIN_URL + str(INDEXER_PORT) + "/"
text_processing_url = MAIN_URL + str(TEXT_PROCESSING_PORT) + "/"
ranking_url = MAIN_URL + str(RANKING_PORT) + "/"
snippets_url = MAIN_URL + str(SNIPPETS_PORT) + "/"
res_page_form_url = MAIN_URL + str(RESULT_PAGE_PORT) + "/"
