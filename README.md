# jooble-ir-2018-scissors

### Services adresses
- server_indexer: port=13500
- server_text_processing: port=13501
- server_ranking: port=13502
- server_snippets: port=13503
- server_result_page_form: port=13504
- server_manager: port=13505


###  When you run system for the first time, to build and save an index:
- run server_indexer.py and server_text_processing.py
- run main_index_formation.py to load 5000 documents to index and save it
- run server_ranking.py to create and save tf-idf presentation of documents
- run others "server" scripts