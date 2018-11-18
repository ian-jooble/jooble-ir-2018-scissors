import json
import gzip
import os

import requests
import pandas as pd

r = requests.post('http://127.0.0.1:5000/', json={"search_word": "водител"})
print(r.status_code)
print(r.text)

r = requests.post('http://127.0.0.1:5000/normalization',
                  json={"title": "Садоводство",
                        "text": "Саженцы декоративных и плодовых культур. "
                                "Могилев. Гарантия."})
print(r.status_code)
print(r.text)
#--------##--------##--------##--------##--------##--------##--------##--------#
