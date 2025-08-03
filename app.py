# app.py

from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import analyze_local_sentiment

# Initialize Flask app
app = Flask("Sentiment Analyzer")

@app.route("/")
def render_index_page():
    ''' Renders the index page '''
    return render_template('index.html')

@app.route("/sentimentAnalyzer", methods=["GET"])
def sentiment_analyzer():
    '''
    Receives input text from the frontend, 
    performs sentiment analysis using a local model,
    and returns the label and score.
    '''
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:
        return "No text provided! Please enter some text.", 400

    # Analyze the sentiment locally
    result = analyze_local_sentiment(text_to_analyze)

    # Extract results
    label = result["label"]
    score = result["score"]

    return f"The given text has been identified as {label} with a score of {score}."

if __name__ == "__main__":
    '''
    Runs the Flask app on localhost at port 5000
    '''
    app.run(host="0.0.0.0", port=5000)
