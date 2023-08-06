import numpy as np

from pyranker.preprocessing.tokenizer import tokenize

from . import TfIdfWeighter


class BM25Ranker(TfIdfWeighter):
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.doc_len = []
        self.k1 = k1
        self.b = b
        TfIdfWeighter.__init__(self, corpus, tokenize)
        self.doc_len = np.array(self.doc_len)

    def _initialize(self, doc):
        self.doc_len.append(len(doc))
        super()._initialize(doc)

    def _calc_idf(self):
        """
        Gets the idf score of all terms
        """
        for word, freq in self.word_freq.items():
            self.idf[word] = np.log2(self.corpus_size - freq + 0.5) - np.log2(
                freq + 0.5
            )

    def get_scores(self, query, prune=0):
        """
        Gets the tf-idf of all documents w.r.t. query
        The function doesn't normalize the scores
        """
        score = np.zeros(self.corpus_size)
        avg_dl = sum(self.doc_len) / self.corpus_size
        for word in self.tokenizer(query):
            if self.idf.get(word, 0) < prune:
                continue
            q_freq = np.array([doc.get(word, 0) for doc in self.doc_freqs])
            score += self.idf.get(word, 0) * (
                q_freq
                * (self.k1 + 1)
                / (q_freq + self.k1 * (1 - self.b + self.b * self.doc_len / avg_dl))
            )

        if score.sum() == 0:
            raise ValueError("Either query is empty or all words are pruned")
        return score

    def get_top_n(self, query, n=5, prune=0):
        """
        Get top n documents ranked by tf-idf
        """
        scores = self.get_scores(query, prune)
        return np.argsort(scores)[::-1][:n], scores
