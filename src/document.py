"""Module documents contains class Document"""

import re


class Document:
    """Class for storing different information about a document."""
    
    def __init__(self, doc_id, title, text, language=None):
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
        self.title_normalized = None
        self.text_normalized = None
        self.snippet = None
        self.url = None
        
    def __str__(self):
        return str(self.__dict__)

    def to_dict(self):
        """
        Transform instance of class to dictionary.
        
        :return dict: Dictionary with class attributes and values.
        """
        return self.__dict__
    
    def __repr__(self):
        short_repr = "Title: " + self.title + "\n" + \
                     "Text: " + self.text + "\n" + \
                     "Snippet: " + str(self.snippet) + "\n"
        return short_repr


class ExtendedDocument:
    """
    Class for storing additional information about a document
    which is used for smart ranking and snippets creation.
    """
    def __init__(self, doc_id):
        self.id = doc_id
        self.text_lemmas = ""
        self.text_lemmas_tags = ""
        self.requirement = ""
        self.requirement_normalized = ""
        self.requirement_lemmas = ""
        self.requirement_lemmas_tags = ""
        self.prof_area = ""
        self.prof_area_id = ""
        self.prof_area_normalized = ""
        self.prof_area_lemmas = ""
        self.prof_area_lemmas_tags = ""

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        short_repr = "id: " + self.id + "\n" + \
                     "Text_lemmas: " + self.text_lemmas + "\n" + \
                     "Requirement lemmas: " + str(self.requirement_lemmas) + "\n" + \
                     "Professional area: " + str(self.prof_area) + "\n"
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


