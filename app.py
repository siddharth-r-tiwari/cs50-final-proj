#import flask 
import os

from flask import Flask, flash, redirect, render_template, request

#import helper functions
from helpers import *

#app creation and configuration
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
    """static route for displaying 'about' page"""
    return render_template("about.html")

@app.route("/", methods=["GET", "POST"])
def index():
    """route for displaying homepage"""

    #dictionary to store retrieved and processed data
    queries = {}

    #if user inputs a request, retrieve data from form from homepage
    if request.method == "POST":
        #four parameters: date_start: starting date of date range, date_end: end date of date range, n: number of steps, url: url being queried
        date_start = get_dtSTEP(request.form.get("date_start") + " 00:00:00")
        date_end = get_dtSTEP(request.form.get("date_end") + " 00:00:00")
        n = int(request.form.get("n"))
        url  = request.form.get("url")
    #on start up, query a website (fox news in this case) and produce 4 visualizations with the date range of a year prior to now
    else:
        date_start = get_dtSTEP(str(get_date_start()))
        date_end = get_dtSTEP(str(get_date_end()))
        n = 4
        url = 'https://www.foxnews.com/'

    #obtain date range for querying (dates array)
    dates = get_dates(date_start, date_end, n)

    #handle user input errors (invalid date range, invalid steps)
    if dates == "DateError":
        queries = {'Error': 'Invalid date range entered; please make sure the start AND end date are in the past, and the start date comes before the end date.'}
    elif n <= 0 or n%1 != 0:
        queries = {'Error': 'Invalid step size entered; please make sure an integer greater than zero is entered.'}
    else:
        #query each of the dates
        for i in range(1, n+1):
            #each query was assigned a number 1 to n, corresponding to their chronological placement
            queries[str(i)] = {}
            queries[str(i)]['newssite'] = url
            queries[str(i)]['date_queried'] = dates[i - 1]

            #call api using url and the date within the dates array
            rq = call_api(url, dates[i - 1])
                
            #if no response, produce error
            if rq == {}:
                queries[str(i)]['Error'] = "Oh no, Error in API Response :<"
            else:
                #obtain url for HTML extraction
                snapshotUrl = get_snapshoturl(rq)

                #if no URL, produce an error
                if not snapshotUrl:
                    queries[str(i)]['Error'] = "Oh no, Error in API Response :<"
                    
                else:
                    #store returned date
                    queries[str(i)]['date_returned'] = WBMtoDT(get_snapshotdate(rq))

                    #extract HTML
                    html = get_HTML(snapshotUrl)

                    #if problem with decoding, produce error
                    if html == "ParsingError":
                        queries[str(i)]['Error'] = "Err, Error Parsing HTML :{"
                    else:
                        #obtain text
                        text = get_text(html)

                        #if problem with scraping, produce error
                        if text == "ScrapingError":
                            queries[str(i)]['Error'] = "Aw man, problem in scraping text :/"
                        else:
                            #analyze texts and produce formattable data for visualizations
                            len_text = [len(phrase) for phrase in text]
                            sentiments = get_sentiments(text)
                            data = format_data(len_text, sentiments)

                            #store processed data within queries dictionary
                            phrases = {'text': text, 'sentiments': sentiments}
                            queries[str(i)]['phrases'] = phrases
                            queries[str(i)]['len_text_formatted'] = data['len_text']
                            queries[str(i)]['sentiments_formatted'] = data['sentiments']

                            #if limited scraped data, produce error
                            if(len(data['sentiments']) < 4):
                                queries[str(i)]['Error'] = "Limited scraped data; try a new date range :["

                    #if caught redirects, produce corresponding errors
                    for index in capture_redirects(queries):
                        queries[index]['Error'] = "Oh no, API Response was redirected :<"
    
    #return HTML and send processed data
    return render_template("index.html", queries=queries)

