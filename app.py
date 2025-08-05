from flask import Flask, render_template, request, jsonify
from SentimentAnalysis.sentiment_analysis import analyze_local_sentiment

# Initialize Flask app
app = Flask("Sentiment Analyzer")

@app.route("/")
def render_index_page():
    ''' Renders the index page '''
    return render_template('index.html')

@app.route("/sentimentAnalyzer", methods=["GET"])
def sentiment_analyzer():
    # Get text input from frontend
    text_to_analyze = request.args.get('textToAnalyze')

    # Analyze using local BERT model
    result = analyze_local_sentiment(text_to_analyze)

    # Return as JSON for front-end JavaScript to style it
    return jsonify(result)

if __name__ == "__main__":
    '''
    Runs the Flask app on localhost at port 5000
    '''
    app.run(host="0.0.0.0", port=5000, debug=True)
