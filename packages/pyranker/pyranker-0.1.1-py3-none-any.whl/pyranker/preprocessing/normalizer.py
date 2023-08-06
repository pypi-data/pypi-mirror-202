import string

from nltk.stem import PorterStemmer


def lowercasing(x: str) -> str:
    return x.lower()


def remove_punctuation(x: str) -> str:
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    return x.translate(translator)


def strip_whitespaces(x: str) -> str:
    x = x.strip()
    while "  " in x:
        x = x.replace("  ", " ")

    return x


def stemmer(x: str) -> str:
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in x.split(" ")]
