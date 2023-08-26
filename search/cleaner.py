import re
import string

def lowercase(tokens):
    return [token.lower() for token in tokens]

def tokenize(text):
    return text.split()

def punctuation(tokens):
    punc = re.compile('[%s]' % re.escape(string.punctuation))
    return [punc.sub('', token) for token in tokens]


def clean(text):
    '''
        tokenise , lower case & remove puntuations
    '''
    tokens = tokenize(text)
    tokens = lowercase(tokens)
    tokens = punctuation(tokens)

    return [token for token in tokens if token]
