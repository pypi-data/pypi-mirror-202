import numpy as np

from pyranker.preprocessing.tokenizer import tokenize

from . import TfIdfWeighter


class VSpaceRanker(TfIdfWeighter):
    def __init__(self, corpus):
        super().__init__(corpus, tokenize)

    def get_vector_dim(self, prune=0):
        """
        Gets the dimension of the vector space
        """
        return sum(1 for v in self.idf.values() if v >= prune)

    def get_scores(self, query, prune=0):
        """
        Gets the cosine scores of all documents w.r.t. query
        Configuration is lnc.lnc
        """
        score = np.empty(shape=(0, self.corpus_size))
        q_score = []
        query = self._calc_freq(self.tokenizer(query))
        for word in self.word_freq.keys():
            if self.idf.get(word, 0) < prune:
                continue
            q_score.append(self.idf.get(word, 0) * query.get(word, 0))
            d_freq = np.array([doc.get(word, 0) for doc in self.doc_freqs])
            score = np.vstack((score, self.idf.get(word, 0) * d_freq))

        # Normalize scores
        norm_val = np.linalg.norm(q_score)
        if norm_val == 0:
            raise ValueError("Either query is empty or all words are pruned")
        q_score = q_score / norm_val
        score = score / np.linalg.norm(score, axis=0)
        # Calculate cosine score
        return np.dot(q_score.T, score).flatten()

    def get_top_n(self, query, n=5, prune=0):
        """
        Get top n documents ranked by tf-idf
        """
        scores = self.get_scores(query, prune)
        return np.argsort(scores)[::-1][:n], scores
