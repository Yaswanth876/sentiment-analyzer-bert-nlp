import requests
import json

def sentiment_analyzer(text_to_analyse):
    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'

    # Create the payload with the text to be analyzed
    payload = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    # Set the headers with the required model ID for the API
    headers = {
        "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
    }

    try:
        # Make a POST request to the API with the payload and headers
        response = requests.post(url, json=payload, headers=headers)

        # Raise an HTTPError if status code is not 200
        response.raise_for_status()

        # Parse the response from the API
        data = response.json()

        # Extract the label and score from the JSON response
        label = data.get('documentSentiment', {}).get('label')
        score = data.get('documentSentiment', {}).get('score')

        return {'label': label, 'score': score}

    except requests.exceptions.RequestException as e:
        # Print the exception for debugging (optional in production)
        print(f"Request error: {e}")
        return {'label': None, 'score': None}

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors gracefully
        print(f"JSON decode error: {e}")
        return {'label': None, 'score': None}
