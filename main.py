from bs4 import BeautifulSoup
import requests
def func(url):
    web_page = requests.get(url).text
    soup = BeautifulSoup(web_page, 'html.parser')

    corpus = ''
    p_tags = soup.find_all('p')
    for p_tag in p_tags:
        corpus += p_tag.text + ' '

    import re
    from string import punctuation
    def txt_clean(x):
        x = x.lower() #convert to lower case
        x = re.sub('\[.*?\]','', x) #remove [] and anything in between the brackets
        x = re.sub('\(.*?\)', '',x)
        x = re.sub('www\S+|https?\S+', '', x) #remove links
        x = re.sub('\<.*?\>', '', x) #remove html tags
        x = re.sub(f'[{re.escape(punctuation)}]', '',x) #remove punctuations
        x = re.sub('\n ','',x) #remove new line
        x = re.sub('\\xa0', ' ',x)
        return x

    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    clean_sent = [txt_clean(sent) for sent in sent_tokenize(corpus)]


    word_freq = {}
    for sent in clean_sent:
        for word in word_tokenize(sent):
            if word in stop:
                try:
                    word_freq[word] += 1
                except KeyError:
                    word_freq[word] = 1

    max_freq = max(word_freq.values())
    norm_freq = {}

    for key, value in word_freq.items():
        norm_freq[key] = value/max_freq

    sent_score = {}
    score = 0

    for sent in clean_sent:
        for word in word_tokenize(sent):
            try:
                score += norm_freq[word]
            except KeyError:
                pass
        sent_score[sent] = score
        score = 0
    n = 10

    from heapq import nlargest
    summary = nlargest(n, iterable=sent_score, key=sent_score.get)
    return '.'.join(summary)
