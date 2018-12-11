"""Module documents contains class Document"""

import re

class Document:
    """Class for storing different information about a document."""
    
    def __init__(self, doc_id, title, text, language, title_normalized,
                text_normalized, url, requirement_normalized="", prof_area="",
                prof_area_normalized=""):
        """
        Create document.

        :param str doc_id:
        :param str title:
        :param str text:
        :param str language: Default None.
        """
        self.id = doc_id
        self.title = title
        self.text = text
        self.language = language
        self.title_normalized = title_normalized
        self.text_normalized = text_normalized
        self.url = url
        self.requirement_normalized = requirement_normalized
        self.prof_area_normalized = prof_area_normalized 
        self.prof_area = prof_area
        self.snippet = ""

    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        short_repr = "Title: " + self.title + "\n" + \
                     "Text: " + self.text + "\n" + \
                     "Snippet: " + str(self.snippet) + "\n"
        return short_repr


class DocumentTermsInfo:
    """
    Class that contains positions for all tokens in text.

    "pos": [list of int], "pos_raw": [list of int]}
    """
    def __init__(self, document):
        self.id = document.id
        self.tokens = {}

        tokens = document.text_normalized.split(" ")
        for token in tokens:
            positions_raw = [string.start() for string
                             in re.finditer(token, document.text)]
            positions = [string.start() for string
                         in re.finditer(token, document.text_normalized)]
            self.tokens[token] = {"pos": positions, "pos_raw": positions_raw}

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        short_repr = str(self.tokens.keys())
        return short_repr


