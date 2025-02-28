import json
import requests
import logging
from html2text import HTML2Text

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Fetches and extracts text content from a webpage."""
    try:
        # Extract URL from event payload
        url = event["url"]
        logger.info(f"Fetching content from: {url}")

        # Custom headers to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        # Perform HTTP request with custom headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Ensure request was successful

        # Convert HTML to clean text
        h = HTML2Text()
        h.ignore_links = True
        text_content = h.handle(response.text)

        # Truncate if too long
        cleaned_text = text_content[:4000] if len(text_content) > 4000 else text_content

        return {
            "statusCode": 200,
            "body": json.dumps({"text": cleaned_text})
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
