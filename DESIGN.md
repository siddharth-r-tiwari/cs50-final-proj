# Essence: Design Document
### The Essence of Digital News Media: A Dynamic, Longitudinal Visualization of Sentiment and Topics

## Fundamentals
At it's core, Essence is a method of data retrieval and processing. Given specific inputs, the program has to both obtain data in line with these inputs and format them in such a way that the user can interact in an informative and undemanding manner. As this is a web-based application that utilizes user inputs to obtain data from APIs and then modify the UI/UX experience, a combination of server-side and client-side source code is used to construct a **pipeline** of queried data. The **pipeline**, after obtaining inputs, is as follows:

1. Send (several) requests for historical webpages of newssites, given the date and url
2. Extract the text from historical webpages
3. Perform a sentiment analysis of the text
4. Create a dynamic, interactable UI for the user using text and subsequent analyses

### Files
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

