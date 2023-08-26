from collections import Counter

from .cleaner import clean

class Document:
    '''
        Document class:
        path = path of document
        text = stuff written in document
        term_frequencies = TF of terms in this doc
    '''
    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.term_frequencies = Counter(clean(self.text))
    
    def fulltext(self):
        return self.text
    
    def path(self):
        return self.path
    
    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)
