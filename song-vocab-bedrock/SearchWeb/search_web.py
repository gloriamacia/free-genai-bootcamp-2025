import json
import logging
from duckduckgo_search import DDGS

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Searches the web for song lyrics using DuckDuckGo."""
    try:
        query = event["query"]
        logger.info(f"Searching for: {query}")

        results = DDGS().text(query + " lyrics", max_results=5)

        search_results = [{"title": result["title"], "url": result["href"]} for result in results]

        return {
            "statusCode": 200,
            "body": json.dumps(search_results)
        }

    except Exception as e:
        logger.error(f"Error in search_web: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
