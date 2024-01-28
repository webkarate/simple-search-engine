import os
import nltk
import sys
from spacy import load

def get_words_from_txt(path):
    array = []
    if not os.path.exists(path):
        print('[Error] File {0} wasn\'t found'.format(path))
        return []

    with open(path, 'r', encoding="utf8") as text:
        text = text.read().split(' ')
        for word in text:
            array.append(word)

    return array


class SingletonClass(object):

  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance


class Search:
    _instance = None

    def __init__(self):
        self.nlp = load("en_core_web_sm")
        self.load_blacklist()
        self.load_efficient_tags()


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Search, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def get_word_lemma(self, word):
        return self.nlp(word)[0].lemma_


    def get_efficient_words_from_text(self, text):
        text = nltk.word_tokenize(text.lower())
        text = nltk.pos_tag(text)
        frequency = {}
        for word in text:
            if word[1] in self.efficient_tags:
                if word[0] not in self.blacklist:
                    lemma = self.get_word_lemma(word[0])
                    if lemma not in frequency.keys():
                        frequency[lemma] = 0

                    frequency[lemma] += 1

        return frequency


    def load_blacklist(self):
        BLACK_LIST_NAME = 'blacklist.txt'
        path = os.path.join(sys.path[0], BLACK_LIST_NAME)
        self.blacklist = get_words_from_txt(path)


    def load_efficient_tags(self):
        EFFICIENT_TAGS_NAME = 'efficient_tags.txt'
        path = os.path.join(sys.path[0], EFFICIENT_TAGS_NAME)
        self.efficient_tags = get_words_from_txt(path)