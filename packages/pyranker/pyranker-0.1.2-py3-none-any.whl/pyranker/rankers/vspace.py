import numpy as np
from preprocessing.tokenizer import tokenize

from . import TfIdfWeighter


class VSpaceRanker(TfIdfWeighter):
    def __init__(self, corpus):
        super().__init__(corpus, tokenize)

    def get_scores(self, query):
        """
        Gets the cosine scores of all documents w.r.t. query
        Default configuration is lnc.ltc
        """
        score = np.empty(shape=(0, self.corpus_size))
        q_score = []
        query = self._calc_freq(self.tokenizer(query))
        for word in self.word_freq.keys():
            q_score.append(self.idf.get(word, 0) * query.get(word, 0))
            d_freq = np.array([doc.get(word, 0) for doc in self.doc_freqs])
            score = np.vstack((score, self.idf.get(word, 0) * d_freq))

        # Normalize scores
        q_score = q_score / np.linalg.norm(q_score)
        score = score / np.linalg.norm(score, axis=0)
        # Calculate cosine score
        return np.dot(q_score.T, score).flatten()

    def get_top_n(self, query, n=5):
        """
        Get top n documents ranked by tf-idf
        """
        scores = self.get_scores(query)
        return np.argsort(scores)[::-1][:n], scores
