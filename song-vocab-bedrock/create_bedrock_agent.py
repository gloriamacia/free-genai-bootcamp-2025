import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS Bedrock client
bedrock_client = boto3.client("bedrock-agent")

# Define agent details
agent_name = "LanguageTutorAgent"
foundation_model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
role_arn = "arn:aws:iam::913524948358:role/BedrockAgentRole"

# Define agent instruction
instruction = """
You are a helpful language tutor. 
When the user provides a song title, search for the song lyrics and help them learn new vocabulary from it. 
First, search for the lyrics, then extract vocabulary from them. 
Explain the meaning of new words in simple terms and provide example sentences. 
Use the user's native language to explain the meaning of new words.
Focus on words that would be valuable for a language learner.
"""

# Function to create a Bedrock Agent
def create_bedrock_agent():
    """Creates an Amazon Bedrock Agent."""
    try:
        response = bedrock_client.create_agent(
            agentName=agent_name,
            foundationModel=foundation_model,
            agentResourceRoleArn=role_arn,
            instruction=instruction,
        )
        agent_id = response["agent"]["agentId"]
        print(f"✅ Successfully created Bedrock Agent: {agent_id}")
        return agent_id
    except Exception as e:
        logger.error(f"❌ Error creating Bedrock Agent: {e}")
        return None

# Run the function
agent_id = create_bedrock_agent()
