#download dependencies
import urllib
from urllib.parse import unquote
import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import numpy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def get_date_start():

    return datetime(
    year=date.today().year, 
    month=date.today().month,
    day=date.today().day) + timedelta(weeks=-52)

def get_date_end():
    return datetime(
    year=date.today().year, 
    month=date.today().month,
    day=date.today().day)

def get_dates(date_start, date_end, n):
    dates = []
    if date_end > get_date_end() or date_start > get_date_end() or date_start >= date_end:
        return "DateError"
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

#def validate_queries(queries):
#    valid_queries = []
#    for query in queries:
#        if query['date_queried'] - query['date_returned'] > 
#    return valid_queries

def get_HTML(url):
    if not url:
        return False

    fp = urllib.request.urlopen(unquote(url))
    inbytes = fp.read()

    #https://stackoverflow.com/questions/46000191/utf-8-codec-cant-decode-byte-0x92-in-position-18-invalid-start-byte
    #https://stackoverflow.com/questions/30598350/unicodedecodeerror-charmap-codec-cant-decode-byte-0x8d-in-position-7240-cha
    try:
        html= inbytes.decode("utf-8")
    except UnicodeDecodeError:
        html = "ParsingError"
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
            if (len(item.get_text().strip()) <= 200 and len(item.get_text().strip()) > 10) and (not("The Archive Team" in item.get_text().strip()) and not ("Wayback Machine" in item.get_text().strip()) and not ("Panic Downloads" in item.get_text().strip()) and not ("archivebot process" in item.get_text().strip())) and not (item.get_text().strip() in text):
                text.append(item.get_text().strip())
    text.sort(key=len, reverse=True)
    if(len(text) < 5):
        return "ScrapingError"
    else:
        return text

def capture_redirects(queries):
    errors = []
    for index in queries.keys():
        if(((queries[index]['date_returned'] - queries[index]['date_queried']) > timedelta(weeks=10)) and ((get_date_end() - queries[index]['date_returned']) < timedelta(weeks=1))):
            errors.append(index)
    return errors

def get_sentiments(text):
    sia = SentimentIntensityAnalyzer()
    sentiments = []

    for phrase in text:
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

def get_dtSTEP(dt):
    """convert date to steppable format"""
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

def WBMtoDT(date):
    return datetime.strptime(date, "%Y%m%d%H%M%S")

