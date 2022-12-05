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
        date_start = get_dtSTEP(request.form.get("date_start"))
        date_end = get_dtSTEP(request.form.get("date_end"))
        n = int(request.form.get("n"))
        url  = request.form.get("url")
    
    else:
        date_start = get_date_start()
        date_end = get_date_end()
        n = 4
        url = 'https://www.foxnews.com/'

    dates = get_dates(date_start, date_end, n)
    parameters = [n, url, dates]

    for i in range(1, n+1):
        queries[str(i)] = {}
        queries[str(i)]['newssite'] = url
        queries[str(i)]['date_queried'] = dates[i - 1]

        rq = call_api(url, dates[i - 1])
            
        if rq == {}:
            flash("No API Response")
            queries[str(i)]['response'] = "No API Response"
        else:
            snapshotUrl = get_snapshoturl(rq)

            if not snapshotUrl:
                flash("No Snapshot URL returned")
                queries[str(i)]['response'] = "No Snapshot URL returned"
                
            else:
                queries[str(i)]['date_returned'] = get_snapshotdate(rq)
                html = get_HTML(snapshotUrl)
                text = get_text(html)
                len_text = [len(phrase) for phrase in text]
                sentiments = get_sentiments(text)
                data = format_data(len_text, sentiments)

                phrases = {'text': text, 'sentiments': sentiments}
                queries[str(i)]['phrases'] = phrases
                queries[str(i)]['len_text_formatted'] = data['len_text']
                queries[str(i)]['sentiments_formatted'] = data['sentiments']
            
                #https://stackoverflow.com/questions/72076666/create-a-dictionary-from-multiple-lists-one-list-as-key-other-as-value

    return render_template("index.html", queries=queries)

