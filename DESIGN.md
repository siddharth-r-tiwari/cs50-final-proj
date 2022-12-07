# Essence: Design Document
### The Essence of Digital News Media: A Dynamic, Longitudinal Visualization of Sentiment and Topics

## Fundamentals
At it's core, Essence is a method of data retrieval and processing. Given specific inputs, the program has to both obtain data in line with these inputs and format them in such a way that the user can interact in an informative and undemanding manner. As this is a web-based application that utilizes user inputs to obtain data from APIs and then modify the UI/UX experience, a combination of server-side and client-side source code is used to construct a **pipeline** of queried data. The **pipeline**, after obtaining inputs, is as follows:

1. Send (several) requests for historical webpages of newssites, given the date and url
2. Extract the text from historical webpages
3. Perform a sentiment analysis of the text
4. Create a dynamic, interactable UI for the user using text and subsequent analyses

Within this pipeline are several considerations for how to efficiently process and transfer data as well as possible errors that may arise. The following files are utilized in this program:

* `cs50-final-proj/`
    * `README.md`: Readme doc
    * `DESIGN.md`: Design doc
    * `requirements.txt`: Requirements/dependencies for running Essence
    * `app.py`: Application routes, which contain user input processing and the corresponding response
    * `helpers.py`: Helper functions used for the **pipeline** (interacting with APIs, performing text processing and sentiment analysis, and error handling)
    * `templates/`
        * `index.html`: The Program
        * `about.html`: About Page
        * `static/`
            * `scripts.js`: Dynamic front-end functionality (code for the visualization, user-application interactions)
            * `styles.css`: CSS Styling
            * `favicon.png`, `legend.png`, `emotionalismblog.png`: Images used in various parts of the application


As steps 1-3 deal with both the retrieval and heavy processing of data, these tasks were relegated to the python back-end of this project, whose code lies in `app.py` and `helpers.py`. To separate tasks, data- and error-handling was taken care of in  `app.py` to ensure the creation of a useful dictionary for step 4. `helpers.py` contained the specific code for contacting the API, decoding the HTML performing the sentiment analysis, as well as small helper functions (the conversion of dates), whose return values were sent back to `app.py` for storage.

As all this processing is done on the server-side, the subsequent data is sent via the Flask route to the generated web-page's JavaScript file `scripts.js` such that the user can manipulate the processed data with Essence's available functions, however they may choose. Any errors are also informed to the user so that there is full transparency of Essence's function.

### Requests, Processing, Analysis

WayBackMachine, BeautifulSoup, and NLTK's SentimentIntensityAnalyzer were primarily used for data retrieval and visualization. 
WayBackMachine was the source of all the webpage data, whose API could be used for querying webpages at a specific historical date. Webpage URLs were restricted for the scope of this project, as, in essence, any URL could be requested for the analysis that Essence does; this program can be modified to use any URLs, but the most relevant, reliable, and available newssite URLs were used for this project.
Upon the querying and response of the API, the url and corrresponding HTML was processed using BeautifulSoup so that only the text was extracted. This was challenging, given that a lot of formatting and historical text complicates the scraping of these pages. 
After retrieving these phrases, a pre-trained NLTK sentiment analyzing model was used (the VADER model) to obtain compound, sentiment scores for the phrases extracted from the webpages.
As the API has issues with reliability and complexities arose from scraping/encoding, several measures were taken to deal with errors, which are detailed below.

The code for the specific functions within the retrieval, processing, and analysis are detailed within the files themselves.

### Visualization

The HTML Canvas attribute was used dynamically through JavaScript for the creation of the visualizations in Essence. Through the aid of parametrized and asynchronous functions, the user can repeatedly use different variations of these functions to view the visualization and associated phrases in different manners. The data from the previous steps was formatted so that numeric values and phrases were easily iterated and displayed; errors were also documented in a manner that allowed for easy displaying.

### Error Handling
As the pipeline to retrieve and produce usable data contained several steps, here is a list of possible errors that were handled:
* User Inputs:
    * Incorrect Date Range
    * Incorrect Step Size
    * Incorrect URLs: The first thought was to expand usage to all websites, but was restricted to 10 URLs for relevancy, reliability, and availability
* API response and data:
    * No API Response/No URL given for HTML extraction
    * Error with Decoding HTML: Try-Except Block was used in the case of improper decoding
    * Limited phrases decoded/scraped: Message was given to the user if less than five presentable phrases resulted from the pipeline
    * Redirects: This was an error specific to the WayBackScraper API; if a website has a paywall or the API malfunctions, the API would return the most recent webpage rather than the webpage closest to the date requested.
