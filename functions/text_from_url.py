"""
This module takes a URL cleans it and returns the cleaned text
"""
from bs4 import BeautifulSoup
import requests
import re
from string import punctuation
from nltk.tokenize import sent_tokenize

def txt_clean(x):
    """this function cleans the text data from a URL"""

    x = re.sub('\[.*?\]', '', x)  # remove [] and anything in between the brackets
    x = re.sub('\(.*?\)', '', x)
    x = re.sub('www\S+|https?\S+', '', x)  # remove links
    x = re.sub('\<.*?\>', '', x)  # remove html tags
    x = re.sub(f'[{re.escape(punctuation)}]', '', x)  # remove punctuations
    x = re.sub('\n ', '', x)  # remove new line
    x = re.sub('\\xa0', ' ', x)
    return x


def url_to_text(url):
    """
    This function takes a URL as input and returns the content
    of the website as string text
    """
    web_page = requests.get(url).text
    soup = BeautifulSoup(web_page, 'html.parser')
    corpus = ''
    p_tags = soup.find_all('p')
    for p_tag in p_tags:
        corpus += p_tag.text + ' '

    clean_sent = [txt_clean(sent) for sent in sent_tokenize(corpus)]

    corpus = '. '.join(clean_sent)
    return corpus
