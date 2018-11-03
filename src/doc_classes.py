"""Module documents contains class Document"""
import json
    
class Document():
    """Class for storing different information about a document."""
    
    def __init__(self, **kwargs):
        """
        Transform values of dictionary kwargs to class attributes.
        """
        self.__dict__.update(kwargs)

        
    def __str__(self):
        return str(self.__dict__)
    
    
    def to_dict(self):
        """
        Transform instance of class to dictionary.
        Returns:
        dictionary with class attributes and values
        """
        return self.__dict__
      
        
    def toJSON(self):
        """
        Transform instance of class to json format.
        Returns:
        string
        """
        return json.dumps(self, default=lambda obj: obj.__dict__)
    