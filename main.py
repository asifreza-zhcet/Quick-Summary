"""
This module is used to calculate sentence score and return the summary
"""

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from heapq import nlargest

stop = stopwords.words('english')


def summarize(corpus, n):
    """
    This function first calculates the sentence score based on the frequency of the words and then
    returns the summary based on the sentence scores
    """
    clean_sent = sent_tokenize(corpus)
    # Calculating word frequency
    word_freq = {}
    for sent in clean_sent:
        for word in word_tokenize(sent):
            if word.lower() not in stop:
                try:
                    word_freq[word.lower()] += 1
                except KeyError:
                    word_freq[word.lower()] = 1

    # Normalizing the frequency by dividing with maximum frequency
    max_freq = max(word_freq.values())
    norm_freq = {}
    for key, value in word_freq.items():
        norm_freq[key] = value / max_freq

    # Calculating the sentence scores
    sent_score = {}
    score = 0
    for sent in clean_sent:
        for word in word_tokenize(sent):
            try:
                score += norm_freq[word.lower()]
            except KeyError:
                pass
        sent_score[sent] = score
        score = 0

    # Calculating the size (in number of lines) to be returned as summary
    length = int(len(clean_sent) * n)
    # If the size is 0 the default size of the summary is 1.
    if length == 0:
        length = 1

    summary = nlargest(length, iterable=sent_score, key=sent_score.get)

    return ' '.join(summary)
