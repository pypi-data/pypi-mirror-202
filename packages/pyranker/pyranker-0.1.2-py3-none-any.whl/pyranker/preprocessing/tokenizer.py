from . import normalizer


def tokenize(doc) -> list:
    doc = normalizer.lowercasing(doc)
    doc = normalizer.remove_punctuation(doc)
    doc = normalizer.strip_whitespaces(doc)
    return normalizer.stemmer(doc)
