import urllib
import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import numpy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

#level 1 functions
def get_date_start():
    return get_dtSTEP(str(date.today() + timedelta(weeks=-52)))

def get_date_end():
    return get_dtSTEP(str(date.today()))

def get_dates(date_start, date_end, n):
    dates = []
    span = date_end - date_start
    delta = span/(n-1)
    for i in range(n):
        dates.append(date_start + delta*i)
    return dates

def call_api(url, timestamp):
    parameters = {
        "url": url,
        "timestamp": get_dtWBM(timestamp)
    }

    request = requests.get("http://archive.org/wayback/available",params=parameters)
    
    if request.status_code != 200:
        return {}
    else:
        return request

def get_snapshoturl(request):
    if "closest" in request.json()["archived_snapshots"]:
        return request.json()["archived_snapshots"]["closest"]["url"]
    return False

def get_snapshotdate(request):
    return request.json()["archived_snapshots"]["closest"]["timestamp"]

#def WBMtoDT(date):
#    return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")

def get_HTML(url):
    if not url:
        return False

    fp = urllib.request.urlopen(url)
    inbytes = fp.read()
    html = inbytes.decode("utf-8")
    fp.close()
    return html

def get_text(html):
    if not html:
        return False
    tags = ['h1','h2','h3','h4', 'h5', 'h6','p', 'strong', 'span']
    text = []

    page = BeautifulSoup(html, 'html.parser')
    for tag in tags:
        for item in page.find_all(tag):
            if (len(item.get_text()) <= 200 and len(item.get_text()) > 10) and (not("The Archive Team" in item.get_text()) or not ("Wayback Machine" in item.get_text()) or not ("Panic Downloads" in item.get_text())):
                text.append(item.get_text())
    text.sort(key=len, reverse=True)
    return text


def get_sentiments(text):
    sia = SentimentIntensityAnalyzer()
    sentiments = []

    for phrase in text:
        #if(sia.polarity_scores(phrase)['compound']):
        sentiments.append(sia.polarity_scores(phrase)['compound'])

    return sentiments

def format_data(len_text, sentiments):
    data = {'len_text':[], 'sentiments':[]}
    sentiments_unavg = {}
    for i in range(0, len(len_text)):
        l1 = len_text[i]
        for l2 in data['len_text']:
            if abs(l1 - l2) <= 5:
                sentiments_unavg[str(l2)].append(sentiments[i]) 
                break
        else:
            data['len_text'].append(l1)
            sentiments_unavg[str(l1)] = [sentiments[i]]
            
    for key in sentiments_unavg:
        data['sentiments'].append(sum(sentiments_unavg[key])/len(sentiments_unavg[key]))
    
    return data

#level 2 functions
def get_dtWBM(dt):
    """"""
    return str(dt.year) + str(dt.month) + str(dt.day)

def get_dtSTEP(response):
    """convert date to steppable format"""
    return datetime.strptime(response, "%Y-%m-%d")

