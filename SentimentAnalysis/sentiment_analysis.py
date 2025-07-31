import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# Constants
API_URL = (
    "https://sn-watson-sentiment-bert.labs.skills.network"
    "/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict"
)
MODEL_ID = "sentiment_aggregated-bert-workflow_lang_multi_stock"
HEADERS = {
    "Content-Type": "application/json",
    "grpc-metadata-mm-model-id": MODEL_ID,
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def sentiment_analyzer(
    text: str,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Analyze sentiment of the given text using IBM Watson NLP API.

    Args:
        text: The input string to analyze.
        verbose: If True, logs API response details.

    Returns:
        A dict with keys:
          - text: original text
          - sentiment: 'positive', 'negative', 'neutral', 'invalid', or 'error'
          - confidence: float confidence (0.0–1.0)
    """
    text = text.strip()
    if not text:
        if verbose:
            logger.warning("Received empty text; returning 'invalid' sentiment.")
        return {"text": text, "sentiment": "invalid", "confidence": 0.0}

    payload = {"raw_document": {"text": text}}

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        sentiment_info = data.get("documentSentiment", {})
        sentiment = sentiment_info.get("label", "unknown")
        confidence = float(sentiment_info.get("score", 0.0))

        if verbose:
            logger.debug("API response: %s", json.dumps(sentiment_info, indent=2))

        return {"text": text, "sentiment": sentiment, "confidence": confidence}

    except requests.Timeout:
        logger.error("Request timed out for text: %r", text)
        return {"text": text, "sentiment": "error", "confidence": 0.0}
    except requests.RequestException as e:
        logger.error("Request error: %s", e)
        return {"text": text, "sentiment": "error", "confidence": 0.0}
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to parse JSON response: %s", e)
        return {"text": text, "sentiment": "error", "confidence": 0.0}


def batch_analyze(
    texts: List[str],
    verbose: bool = False
) -> List[Dict[str, Any]]:
    """
    Analyze a list of texts in batch.

    Args:
        texts: List of strings to analyze.
        verbose: If True, logs progress.

    Returns:
        A list of sentiment analysis results.
    """
    results: List[Dict[str, Any]] = []
    total = len(texts)
    for idx, text in enumerate(texts, start=1):
        if verbose:
            logger.info("Processing %d/%d", idx, total)
        results.append(sentiment_analyzer(text, verbose=verbose))
    return results


def load_texts_from_file(filepath: Path) -> List[str]:
    """
    Read lines from a text file, skipping blank lines.
    """
    if not filepath.exists():
        logger.error("File not found: %s", filepath)
        return []
    return [line.strip() for line in filepath.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Multilingual Sentiment Analyzer (IBM Watson)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t", "--text", nargs="+", help="Text strings to analyze."
    )
    group.add_argument(
        "-f", "--file", type=Path, help="Path to a text file with one sentence per line."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    texts: List[str] = []
    if args.text:
        texts = [" ".join(args.text)]
    elif args.file:
        texts = load_texts_from_file(args.file)

    if not texts:
        logger.error("No text provided for sentiment analysis.")
        return

    results = batch_analyze(texts, verbose=args.verbose)
    for res in results:
        sentiment = res.get("sentiment", "error")
        confidence = res.get("confidence", 0.0)
        print(f"Text: {res['text']}\nSentiment: {sentiment} (Confidence: {confidence:.2%})\n")


if __name__ == "__main__":
    main()
