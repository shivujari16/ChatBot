from nltk import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
#from spellchecker import SpellChecker
def tokenize(sentence): #senstence ko tokenize krega
    return word_tokenize(sentence)


stemmer = PorterStemmer()

def stemming(word): #word stemming
    return  stemmer.stem(word.lower())

#spell = SpellChecker()
#def SpellCorrect(words):
#    return str(spell.correction(words))

def bag_of_word(tokenized_sent, all_words):
    tokenized_sent = [stemming(w) for w in tokenized_sent]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sent:
            bag[idx] = 1.0
    return bag
