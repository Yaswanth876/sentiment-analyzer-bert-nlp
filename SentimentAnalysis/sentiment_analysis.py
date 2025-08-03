# SentimentAnalysis/sentiment_analysis.py

from textblob import TextBlob

def analyze_local_sentiment(text):
    '''
    Analyzes sentiment using TextBlob locally.
    Returns a label and polarity score.
    '''
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "label": sentiment,
        "score": round(polarity, 3)
    }
