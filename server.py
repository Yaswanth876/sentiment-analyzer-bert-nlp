from flask import Flask, render_template, request, jsonify
import logging
from pathlib import Path

# Import the analyzer from your module (adjust path as needed)
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

# Flask app configuration
APP = Flask(
    __name__,
    template_folder=Path(__file__).parent / 'templates',
    static_folder=Path(__file__).parent / 'static'
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

@APP.route('/sentiment', methods=['GET'])
def analyze_sentiment():
    """
    Analyze sentiment of the provided text query parameter.

    Query Params:
        text (str): Text to be analyzed.

    Returns:
        JSON: { 'text': str, 'sentiment': str, 'confidence': float }
    """
    text = request.args.get('text', '').strip()
    if not text:
        logger.warning("No text provided for analysis.")
        return jsonify({
            'error': 'No text provided. Please supply ?text=your_text' }
        ), 400

    # Call the analysis function
    result = sentiment_analyzer(text)
    sentiment = result.get('sentiment') or 'error'
    confidence = result.get('confidence') or 0.0

    logger.info("Analyzed text: %r -> %s (%.2f)", text, sentiment, confidence)

    return jsonify({
        'text': text,
        'sentiment': sentiment,
        'confidence': confidence
    })

@APP.route('/', methods=['GET'])
def home():
    """
    Render the home page with the sentiment input form.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Use environment variables or config for host/port in production
    APP.run(host='0.0.0.0', port=5000, debug=False)
