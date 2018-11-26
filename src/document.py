"""Module documents contains class Document"""


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
    
    
class TokenDocumentInfo:
    
    """Class for storing information about token in a particular document."""
    
    def __init__(self, doc_id, pos, pos_raw):
        """     
        :param str doc_id: Id of particular document.
        :param list of int pos: Positions of token in normilized text.
        :param list of int pos_raw: Positions of token in raw text.
        """
        self.id = doc_id
        self.pos = pos
        self.pos_raw = pos_raw
    
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)
 