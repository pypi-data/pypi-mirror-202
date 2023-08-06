from multiprocessing import Pool, cpu_count

import numpy as np


class TfIdfWeighter:
    def __init__(self, corpus, tokenizer=str.split):
        self.corpus_size = len(corpus)
        self.doc_freqs = []
        self.word_freq = {}
        self.idf = {}
        self.tokenizer = tokenizer

        for doc in self._tokenize_corpus(corpus):
            self._initialize(doc)

        self._calc_idf()

    @staticmethod
    def _calc_freq(doc):
        freq = {}
        for word in doc:
            if word not in freq:
                freq[word] = 0
            freq[word] += 1

        return freq

    def _initialize(self, doc):
        freq = self._calc_freq(doc)
        self.doc_freqs.append(freq)

        for word, f in freq.items():
            try:
                self.word_freq[word] += 1
            except KeyError:
                self.word_freq[word] = 1

    def _tokenize_corpus(self, corpus):
        for doc in corpus:
            yield self.tokenizer(doc)

    def _calc_idf(self):
        """
        Gets the idf score of all terms
        """
        corpus_size = np.log2(self.corpus_size)
        for word, freq in self.word_freq.items():
            self.idf[word] = corpus_size - np.log2(freq)
