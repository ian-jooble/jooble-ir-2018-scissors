import os

base_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[:-1][0]
data_dir = os.path.join(base_dir, 'data')
by_dir = os.path.join(data_dir, "by_jobs", "by")

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
SNIPPETS_PATH = "snippets"
RESULT_PAGE_PATH = "result_page"

MAIN_URL = "http://0.0.0.0:"
LEPUS_URL  = "http://0.0.0.0:13505/"

indexer_url = MAIN_URL + str(INDEXER_PORT) + "/"
text_processing_url = MAIN_URL + str(TEXT_PROCESSING_PORT) + "/"
ranking_url = MAIN_URL + str(RANKING_PORT) + "/"
snippets_url = MAIN_URL + str(SNIPPETS_PORT) + "/"
res_page_form_url = MAIN_URL + str(RESULT_PAGE_PORT) + "/"



