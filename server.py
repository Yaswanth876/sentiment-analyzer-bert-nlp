"""
This module starts a Flask web server for performing sentiment analysis
using a pre-trained NLP model through a sentiment analyzer API.

The application exposes two routes:
1. /sentimentAnalyzer : Accepts query text and returns sentiment label and score.
2. /                  : Renders the home page (index.html).
"""

# Import Flask, render_template, request from the flask framework package
from flask import Flask, render_template, request
# Import the sentiment_analyzer function from the package created
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

# Initiate the flask app
app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # If user didn’t supply any text
    if not text_to_analyze:
        return "No text provided! Try again."

    # Pass the text to the sentiment_analyzer function and store the response
    response = sentiment_analyzer(text_to_analyze)

    # Extract the sentiment and confidence from the response
    sentiment = response.get('sentiment')
    confidence = response.get('confidence')

    # Check if the analyzer returned an error
    if sentiment is None or confidence is None:
        return "Invalid input or analysis error! Try again."

    # Return a formatted string with the sentiment and score
    return f"The given text has been identified as {sentiment} with a score of {confidence}."

    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analyzer()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    # TODO

@app.route("/")
def render_index_page():
    return render_template('index.html')

    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    # TODO

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    ''' This function executes the flask app and deploys it on localhost:5000
    '''
    # TODO
