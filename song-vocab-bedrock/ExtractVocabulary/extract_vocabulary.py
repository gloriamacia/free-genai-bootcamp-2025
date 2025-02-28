import json
import logging
import re
import os
import nltk
from nltk.corpus import stopwords

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set NLTK data path to `/tmp` (Lambda's writable directory)
nltk.data.path.append("/tmp")

# Download stopwords if not already present
if not os.path.exists("/tmp/corpora/stopwords"):
    nltk.download("stopwords", download_dir="/tmp")

def lambda_handler(event, context):
    """Extracts important vocabulary words from lyrics."""
    try:
        # Extract text from event payload
        text = event["text"]
        logger.info("Extracting vocabulary...")

        # Convert text to lowercase and split into words
        words = set(re.findall(r"\b[a-zA-ZäöüßÄÖÜ]+\b", text.lower()))

        # Load stopwords for filtering (English & German)
        stop_words = set(stopwords.words("english") + stopwords.words("german"))

        # Filter out stopwords and short words (length < 3)
        vocabulary = sorted([word for word in words if word not in stop_words and len(word) > 2])

        return {
            "statusCode": 200,
            "body": json.dumps({"vocabulary": vocabulary})
        }

    except Exception as e:
        logger.error(f"Error in extract_vocabulary: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
