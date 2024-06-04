from bs4 import BeautifulSoup
import requests
import re
from string import punctuation
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from heapq import nlargest

nltk.download("stopwords")

stop = stopwords.words('english')

def txt_clean(x):
    '''this function cleans the text'''
   
    x = re.sub('\[.*?\]','', x) #remove [] and anything in between the brackets
    x = re.sub('\(.*?\)', '',x)
    x = re.sub('www\S+|https?\S+', '', x) #remove links
    x = re.sub('\<.*?\>', '', x) #remove html tags
    x = re.sub(f'[{re.escape(punctuation)}]', '',x) #remove punctuations
    x = re.sub('\n ','',x) #remove new line
    x = re.sub('\\xa0', ' ',x)
    return x

def func(url, n):
    web_page = requests.get(url).text
    soup = BeautifulSoup(web_page, 'html.parser')

    corpus = ''
    p_tags = soup.find_all('p')
    for p_tag in p_tags:
        corpus += p_tag.text + ' '

    original = sent_tokenize(corpus)
    clean_sent = [txt_clean(sent) for sent in sent_tokenize(corpus)]


    word_freq = {}
    for sent in clean_sent:
        for word in word_tokenize(sent):
            if word.lower() not in stop:
                try:
                    word_freq[word.lower()] += 1
                except KeyError:
                    word_freq[word.lower()] = 1

    max_freq = max(word_freq.values())

    norm_freq = {}

    for key, value in word_freq.items():
        norm_freq[key] = value/max_freq

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
    
    length = int(len(clean_sent) * n)

    
    summary = nlargest(length, iterable=sent_score, key=sent_score.get)
    return '.'.join(summary)
