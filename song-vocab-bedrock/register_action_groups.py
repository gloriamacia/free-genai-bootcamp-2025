import boto3
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Bedrock Agent client
bedrock_client = boto3.client("bedrock-agent")

# Your Bedrock Agent details
agent_id = "KRSWKL2QPK"   # Replace if needed
agent_version = "DRAFT"    # For agents in draft mode

# Lambda function ARNs for your action groups
lambda_functions = {
    "SearchWeb": "arn:aws:lambda:us-east-1:913524948358:function:SearchWeb",
    "GetPageContent": "arn:aws:lambda:us-east-1:913524948358:function:GetPageContent",
    "ExtractVocabulary": "arn:aws:lambda:us-east-1:913524948358:function:ExtractVocabulary",
}

# Updated YAML definitions for each action group
search_web_yaml = """
openapi: "3.0.0"
info:
  title: "SearchWeb Action"
  version: "1.0.0"
  description: "API for searching the web for song lyrics."
paths:
  /searchweb:
    post:
      summary: "Search song lyrics"
      description: "Search the web for song lyrics based on a song title."
      operationId: "SearchWeb"
      x-toolName: "SearchWeb"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: "The song title to search."
              required:
                - query
      responses:
        "200":
          description: "Successful response"
""".strip()

get_page_content_yaml = """
openapi: "3.0.0"
info:
  title: "GetPageContent Action"
  version: "1.0.0"
  description: "API for fetching the content of a webpage."
paths:
  /getpagecontent:
    post:
      summary: "Get page content"
      description: "Extract text content from a given webpage URL."
      operationId: "GetPageContent"
      x-toolName: "GetPageContent"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                url:
                  type: string
                  description: "The webpage URL to fetch lyrics from."
              required:
                - url
      responses:
        "200":
          description: "Successful response"
""".strip()

extract_vocabulary_yaml = """
openapi: "3.0.0"
info:
  title: "ExtractVocabulary Action"
  version: "1.0.0"
  description: "API for extracting vocabulary from text."
paths:
  /extractvocabulary:
    post:
      summary: "Extract vocabulary"
      description: "Extract useful vocabulary words from provided song lyrics."
      operationId: "ExtractVocabulary"
      x-toolName: "ExtractVocabulary"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                  description: "The song lyrics to analyze."
              required:
                - text
      responses:
        "200":
          description: "Successful response"
""".strip()

# Define the action groups configuration
action_groups = [
    {
        "actionGroupName": "SearchWeb",
        "description": "Search the web for song lyrics.",
        "apiSchema": {"payload": search_web_yaml},
        "actionGroupExecutor": {"lambda": lambda_functions["SearchWeb"]},
    },
    {
        "actionGroupName": "GetPageContent",
        "description": "Extract text from a webpage.",
        "apiSchema": {"payload": get_page_content_yaml},
        "actionGroupExecutor": {"lambda": lambda_functions["GetPageContent"]},
    },
    {
        "actionGroupName": "ExtractVocabulary",
        "description": "Extract useful vocabulary from lyrics.",
        "apiSchema": {"payload": extract_vocabulary_yaml},
        "actionGroupExecutor": {"lambda": lambda_functions["ExtractVocabulary"]},
    }
]

def delete_existing_action_groups():
    """Deletes all existing action groups for the given agent and version."""
    try:
        response = bedrock_client.list_agent_action_groups(
            agentId=agent_id,
            agentVersion=agent_version,
            PaginationConfig={"PageSize": 50}
        )
        groups = response.get("actionGroupSummaries", [])
        for group in groups:
            group_id = group["actionGroupId"]
            group_name = group["actionGroupName"]
            try:
                bedrock_client.delete_agent_action_group(
                    agentId=agent_id,
                    agentVersion=agent_version,
                    actionGroupId=group_id
                )
                logger.info(f"Deleted action group: {group_name} (ID: {group_id})")
                print(f"Deleted action group: {group_name}")
            except Exception as de:
                logger.error(f"Error deleting group {group_name}: {de}")
        # Wait a bit for deletions to propagate
        time.sleep(2)
    except Exception as e:
        logger.error(f"Error listing action groups: {e}")

def register_action_groups():
    """Registers the Lambda functions as Action Groups in the Bedrock Agent."""
    for group in action_groups:
        try:
            response = bedrock_client.create_agent_action_group(
                actionGroupName=group["actionGroupName"],
                description=group["description"],
                agentId=agent_id,
                agentVersion=agent_version,
                actionGroupExecutor=group["actionGroupExecutor"],
                apiSchema=group["apiSchema"],
            )
            logger.info(f"Successfully registered action group: {group['actionGroupName']}")
            print(f"Successfully registered action group: {group['actionGroupName']}")
        except Exception as e:
            logger.error(f"Error registering action group {group['actionGroupName']}: {e}")
            print(f"Error registering action group {group['actionGroupName']}: {e}")

if __name__ == "__main__":
    print("Registering new action groups...")
    register_action_groups()
