import urllib
import requests
import datetime
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def get_dtWBM(dt):
    """"""
    return str(dt.year) + str(dt.month) + str(dt.day)

def get_dtSTEP(response):
    """convert date to steppable format"""
    return datetime.datetime.strptime(response, "%Y-%m-%d")

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

#def getSnapshotAccuracy(request):
#    return request.json()["archived_snapshots"]["closest"]["timestamp"]

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
            if len(item.get_text()) > 10 and (not("The Archive Team" in item.get_text()) or not ("Wayback Machine" in item.get_text()) or not ("Panic Downloads" in item.get_text())):
                text.append(item.get_text())
    return text

def get_sentiments(text):
    sia = SentimentIntensityAnalyzer()
    sentiments = []

    for phrase in text:
        sentiments.append(sia.polarity_scores(phrase)['compound'])

    return sentiments

def get_topics(text):

    return topics