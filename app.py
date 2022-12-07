import os

from flask import Flask, flash, redirect, render_template, request
import pandas as pd

from helpers import *

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app._static_folder = os.path.abspath("templates/static/")
app.config['SECRET_KEY'] = os.urandom(12)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/", methods=["GET", "POST"])
def index():
    #queries = {'0': [url, date_queried, phrases, len_text_formatted, sentiments_formatted]}
    queries = {}


    if request.method == "POST":
        date_start = get_dtSTEP(request.form.get("date_start") + " 00:00:00")
        date_end = get_dtSTEP(request.form.get("date_end") + " 00:00:00")
        n = int(request.form.get("n"))
        url  = request.form.get("url")
    
    else:
        date_start = get_dtSTEP(str(get_date_start()))
        date_end = get_dtSTEP(str(get_date_end()))
        n = 4
        url = 'https://www.foxnews.com/'

    dates = get_dates(date_start, date_end, n)
    if dates == "DateError":
        queries = {'Error': 'Invalid date range entered; please make sure the start AND end date are in the past, and the start date comes before the end date.'}
    elif n <= 0 or n%1 != 0:
        queries = {'Error': 'Invalid step size entered; please make sure an integer greater than zero is entered.'}
    else:
        for i in range(1, n+1):
            queries[str(i)] = {}
            queries[str(i)]['newssite'] = url
            queries[str(i)]['date_queried'] = dates[i - 1]

            rq = call_api(url, dates[i - 1])
                
            if rq == {}:
                queries[str(i)]['Error'] = "Oh no, Error in API Response :<"
            else:
                snapshotUrl = get_snapshoturl(rq)

                if not snapshotUrl:
                    flash("No Snapshot URL returned")
                    queries[str(i)]['Error'] = "Oh no, Error in API Response :<"
                    
                else:
                    queries[str(i)]['date_returned'] = WBMtoDT(get_snapshotdate(rq))
                    html = get_HTML(snapshotUrl)
                    if html == "ParsingError":
                        queries[str(i)]['Error'] = "Err, Error Parsing HTML :{"
                    else:
                        text = get_text(html)
                        if text == "ScrapingError":
                            queries[str(i)]['Error'] = "Aw man, problem in scraping text :/"
                        else:
                            len_text = [len(phrase) for phrase in text]
                            sentiments = get_sentiments(text)
                            data = format_data(len_text, sentiments)

                            phrases = {'text': text, 'sentiments': sentiments}
                            queries[str(i)]['phrases'] = phrases
                            queries[str(i)]['len_text_formatted'] = data['len_text']
                            queries[str(i)]['sentiments_formatted'] = data['sentiments']

                            if(len(data['sentiments']) < 4):
                                queries[str(i)]['Error'] = "Limited scraped data; try a new date range :["

                    for index in capture_redirects(queries):
                        queries[index]['Error'] = "Oh no, API Response was redirected :<"
                        
                            #https://stackoverflow.com/questions/72076666/create-a-dictionary-from-multiple-lists-one-list-as-key-other-as-value

    return render_template("index.html", queries=queries)

