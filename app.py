import os

from flask import Flask, flash, redirect, render_template, request

from helpers import *
import datetime

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app._static_folder = os.path.abspath("templates/static/")

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
    query = {'date_start': 0, 'date_end': 0, 'date_accuracy': 0, 'url': 0, 'request':0, 'response': 0}

    if request.method == "POST":
        query['date_start'] = get_dtSTEP(request.form.get("date_start"))
        query['date_end'] = get_dtSTEP(request.form.get("date_end"))
        query['n'] = request.form.get("n")
        query['url']  = request.form.get("url")
        
        rq = call_api(query['url'], query['date_start'])

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
                sentiments = get_sentiments(text)
                query['response'] = [len(phrase) for phrase in text] + sentiments

                #https://stackoverflow.com/questions/72076666/create-a-dictionary-from-multiple-lists-one-list-as-key-other-as-value
       

    return render_template("index.html", query=query)

