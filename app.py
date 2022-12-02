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
    query = {}

    if request.method == "POST":
        query['date_start'] = get_dtSTEP(request.form.get("date_start"))
        query['date_end'] = get_dtSTEP(request.form.get("date_end"))
        query['n'] = request.form.get("n")
        query['url']  = request.form.get("url")
    
    else:
        query['date_start'] = get_start_date()
        query['date_end'] = get_end_date()
        query['n'] = 2
        query['url'] = 'https://www.npr.org/'

    #dates = get_dates(query['date_start'], query['date_end'], query['n'])
    rq = call_api(query['url'], query['date_start'])
    #for date in dates:
        
    if rq == {}:
        flash("No API Response")
        query['response'] = "No API Response"
    else:
        query['request'] = rq
        snapshotUrl = get_snapshoturl(rq)

        if not snapshotUrl:
            flash("No Snapshot URL returned")
            query['response'] = "No Snapshot URL returned"
            
        else:
            query['date_accuracy'] = get_snapshotdate(rq)
            html = get_HTML(snapshotUrl)
            text = get_text(html)
            len_text = [len(phrase) for phrase in text]
            sentiments = get_sentiments(text)
            data = format_data(len_text, sentiments)

            phrases = {'text': text, 'sentiments': sentiments}
            query['phrases'] = phrases
            query['len_text_formatted'] = data['len_text']
            query['sentiments_formatted'] = data['sentiments']
          
            #https://stackoverflow.com/questions/72076666/create-a-dictionary-from-multiple-lists-one-list-as-key-other-as-value
       

    return render_template("index.html", query=query)

