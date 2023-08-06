import numpy as np
from preprocessing.tokenizer import tokenize

from . import TfIdfWeighter


class TfIdfRanking(TfIdfWeighter):
    def __init__(self, corpus):
        super().__init__(corpus, tokenize)

    def get_scores(self, query):
        """
        Gets the tf-idf of all documents w.r.t. query
        The function doesn't normalize the scores
        """
        score = np.zeros(self.corpus_size)
        for word in self.tokenizer(query):
            q_freq = np.array([doc.get(word, 0) for doc in self.doc_freqs])
            score += self.idf.get(word, 0) * q_freq
        return score

    def get_top_n(self, query, n=5):
        """
        Get top n documents ranked by tf-idf
        """
        scores = self.get_scores(query)
        return np.argsort(scores)[::-1][:n], scores
